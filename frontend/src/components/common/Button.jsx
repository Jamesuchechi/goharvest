export default function Button({ children, className = '', type = 'button', ...props }) {
  return (
    <button className={`btn ${className}`.trim()} type={type} {...props}>
      {children}
    </button>
  );
}
