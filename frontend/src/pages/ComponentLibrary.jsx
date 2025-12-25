import Button from '../components/common/Button.jsx';

export default function ComponentLibrary() {
  return (
    <div className="page">
      <div className="section-header">
        <h2>Component Library</h2>
      </div>
      <div className="panel">
        <p>Browse extracted UI components and bookmark favorites.</p>
        <Button type="button">Filter Components</Button>
      </div>
    </div>
  );
}
