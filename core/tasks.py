import asyncio
import hashlib
import logging

from celery import shared_task
from django.utils import timezone

from .models import (
    AIAnalysis,
    Asset,
    HarvestJob,
    HarvestResult,
    PerformanceMetrics,
)
from .utils.ai_analyzer import AIAnalyzer
from .utils.asset_downloader import AssetDownloader
from .utils.performance_analyzer import PerformanceAnalyzer
from .utils.scraper import WebScraper
from .utils.tech_detector import TechnologyDetector

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def harvest_website(self, job_id):
    try:
        job = HarvestJob.objects.get(id=job_id)
        job.status = 'running'
        job.started_at = timezone.now()
        job.save(update_fields=['status', 'started_at'])

        scraper = WebScraper(url=job.url, options=job.options)
        scraped_data = asyncio.run(scraper.scrape())

        tech_detector = TechnologyDetector(job.url, scraped_data.get('html', ''))
        technologies = tech_detector.detect()

        asset_downloader = AssetDownloader(job.url, scraped_data.get('assets', []))
        downloaded_assets = asyncio.run(asset_downloader.download())

        html = scraped_data.get('html', '')
        content_hash = hashlib.sha256(html.encode()).hexdigest()

        frameworks = technologies.get('frameworks', [])
        css_frameworks = technologies.get('css_frameworks', [])

        result = HarvestResult.objects.create(
            job=job,
            content=scraped_data.get('content', ''),
            html=html,
            structured_data=scraped_data.get('structured', {}),
            assets=downloaded_assets,
            technologies=technologies,
            frontend_framework=frameworks[0] if frameworks else '',
            css_framework=css_frameworks[0] if css_frameworks else '',
            metadata=scraped_data.get('metadata', {}),
            links=scraped_data.get('links', {}),
            content_hash=content_hash,
            total_assets=len(downloaded_assets),
            total_size=sum(asset.get('size', 0) for asset in downloaded_assets),
        )

        for asset_data in downloaded_assets:
            if asset_data.get('status') != 'success':
                continue
            file_name = asset_data.get('file_path', '')
            if file_name.startswith('media/'):
                file_name = file_name.split('media/', 1)[1]
            Asset.objects.create(
                result=result,
                url=asset_data['url'],
                asset_type=asset_data['type'],
                file_size=asset_data.get('size', 0),
                file_path=file_name,
                is_critical=asset_data.get('is_critical', False),
            )

        analyze_performance.delay(result.id)
        perform_ai_analysis.delay(result.id)
        create_zip_export.delay(result.id)

        job.status = 'completed'
        job.completed_at = timezone.now()
        job.save(update_fields=['status', 'completed_at'])

        return {'job_id': str(job_id), 'status': 'completed'}

    except HarvestJob.DoesNotExist:
        logger.error(f"Harvest task failed: job {job_id} not found")
        return {'status': 'failed', 'detail': 'job not found'}
    except Exception as e:
        logger.error(f"Harvest task failed for job {job_id}: {e}")
        job = HarvestJob.objects.filter(id=job_id).first()
        if job:
            job.status = 'failed'
            job.error_message = str(e)
            job.save(update_fields=['status', 'error_message'])
            if job.retry_count < job.max_retries:
                job.retry_count += 1
                job.save(update_fields=['retry_count'])
                raise self.retry(exc=e, countdown=60 * (2 ** job.retry_count))
        raise


@shared_task
def analyze_performance(result_id):
    result = HarvestResult.objects.get(id=result_id)
    analyzer = PerformanceAnalyzer(result.job.url, result.html)
    metrics = analyzer.run_lighthouse()

    PerformanceMetrics.objects.create(
        result=result,
        lighthouse_score=metrics['lighthouse'],
        performance_score=metrics['performance'],
        accessibility_score=metrics['accessibility'],
        best_practices_score=metrics['best_practices'],
        seo_score=metrics['seo'],
        largest_contentful_paint=metrics['lcp'],
        first_input_delay=metrics['fid'],
        cumulative_layout_shift=metrics['cls'],
        time_to_interactive=metrics['tti'],
        total_blocking_time=metrics.get('tbt'),
        total_load_time=metrics['total_time'],
        dom_content_loaded=metrics.get('dom_content_loaded'),
        first_contentful_paint=metrics.get('fcp'),
        total_requests=metrics['requests'],
        total_transfer_size=metrics['transfer_size'],
        resource_breakdown=metrics.get('resource_breakdown', {}),
    )


@shared_task
def perform_ai_analysis(result_id):
    result = HarvestResult.objects.get(id=result_id)
    analyzer = AIAnalyzer(result)
    analysis = analyzer.analyze()

    AIAnalysis.objects.create(
        result=result,
        code_summary=analysis['summary'],
        architecture_analysis=analysis['architecture'],
        component_list=analysis['components'],
        accessibility_score=analysis['a11y_score'],
        seo_score=analysis['seo_score'],
        performance_score=analysis.get('performance_score'),
        seo_suggestions=analysis['seo_suggestions'],
        accessibility_issues=analysis['a11y_issues'],
        security_warnings=analysis['security_warnings'],
        tech_stack_summary=analysis['tech_summary'],
        similar_sites=analysis.get('similar_sites', []),
    )


@shared_task
def create_zip_export(result_id):
    result = HarvestResult.objects.get(id=result_id)
    _ = result
    return None


@shared_task
def schedule_recurring_harvest(job_id, cron_schedule):
    _ = job_id
    _ = cron_schedule
    return None


@shared_task
def check_for_changes(result_id):
    from diff_match_patch import diff_match_patch
    from .models import HarvestSnapshot

    result = HarvestResult.objects.get(id=result_id)
    scraper = WebScraper(result.job.url, result.job.options)
    new_data = asyncio.run(scraper.scrape())

    new_hash = hashlib.sha256(new_data['html'].encode()).hexdigest()
    changes_detected = new_hash != result.content_hash

    snapshot = HarvestSnapshot.objects.create(
        original_result=result,
        content_hash=new_hash,
        changes_detected=changes_detected,
    )

    if changes_detected:
        dmp = diff_match_patch()
        diffs = dmp.diff_main(result.html, new_data['html'])
        snapshot.diff_details = str(diffs)
        snapshot.save(update_fields=['diff_details'])
        if result.job.user_id:
            notify_user_of_changes.delay(result.job.user_id, result_id)

    return changes_detected


@shared_task
def notify_user_of_changes(user_id, result_id):
    _ = user_id
    _ = result_id
    return None
