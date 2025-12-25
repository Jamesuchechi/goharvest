export default function AssetGallery({ assets = [] }) {
  if (!assets.length) {
    return <div className="panel">No assets extracted.</div>;
  }

  return (
    <div className="grid">
      {assets.map((asset) => (
        <div key={asset.url} className="card asset-card">
          <p>{asset.type}</p>
          <small>{asset.url}</small>
        </div>
      ))}
    </div>
  );
}
