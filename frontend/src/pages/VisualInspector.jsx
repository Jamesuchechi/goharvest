import DOMTree from '../components/visualization/DOMTree.jsx';
import PerformanceChart from '../components/visualization/PerformanceChart.jsx';

export default function VisualInspector() {
  return (
    <div className="page">
      <div className="section-header">
        <h2>Visual Inspector</h2>
      </div>
      <div className="grid">
        <DOMTree />
        <PerformanceChart />
      </div>
    </div>
  );
}
