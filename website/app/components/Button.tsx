import c from "../colors";
export default function Button(
  {label, onClick, type="filled"}: 
  {
    label: string, 
    onClick: () => void,
    type?: "filled" | "outlined"
  }) {
  return (
    <button
      style={{...s.button,...s[type]}}
      onClick={onClick}
    >
      {label}
    </button>
  );
}

const s = {
  button:{
    padding: "16px 32px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "24px",
  },
  filled:{
    backgroundColor: c.on_surface_light_gray,
    color: c.on_surface_white,
    fontWeight: "bold",
  },
  outlined: {
    border: `1px solid ${c.border}`,
  }
}