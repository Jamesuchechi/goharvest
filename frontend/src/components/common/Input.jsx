export default function Input({ label, className = '', ...props }) {
  return (
    <label className={`input-field ${className}`.trim()}>
      {label && <span>{label}</span>}
      <input {...props} />
    </label>
  );
}
