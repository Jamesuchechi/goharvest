import asyncio
import logging
import os

from celery import shared_task
from django.core.files import File

from .models import HarvestJob, HarvestResult
from .utils.scraper import WebScraper

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def harvest_website(self, job_id):
    job = None
    zip_path = None
    try:
        job = HarvestJob.objects.get(id=job_id)
        job.status = 'running'
        job.save(update_fields=['status'])

        scraper = WebScraper()
        result_data = asyncio.run(scraper.scrape(job.url, job.options))

        result = HarvestResult(
            job=job,
            content=result_data.get('content', ''),
            html=result_data.get('html', ''),
            assets=result_data.get('assets', []),
            technologies=result_data.get('technologies', {}),
            metadata=result_data.get('metadata', {}),
        )

        zip_path = result_data.get('zip_file')
        if zip_path and os.path.exists(zip_path):
            with open(zip_path, 'rb') as zip_handle:
                result.zip_file.save(os.path.basename(zip_path), File(zip_handle), save=False)

        result.save()

        job.status = 'completed'
        job.save(update_fields=['status'])

        return {'status': 'success', 'result_id': result.id}

    except HarvestJob.DoesNotExist:
        logger.error(f"Harvest task failed: job {job_id} not found")
        return {'status': 'failed', 'detail': 'job not found'}
    except Exception as e:
        logger.error(f"Harvest task failed for job {job_id}: {e}")
        if job:
            job.status = 'failed'
            job.save(update_fields=['status'])
        raise
    finally:
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)
