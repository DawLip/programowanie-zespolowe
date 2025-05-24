import c from "../colors";

/**
 * Komponent Button wyświetlający przycisk z trzema wariantami stylów
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.label - tekst na przycisku
 * @param props.onClick - funkcja wywoływana po kliknięciu przycisku
 * @param props.type - typ przycisku: "filled" | "outlined" | "outlined2" (domyślnie "filled")
 * @returns {JSX.Element} - komponent
 */
export default function Button(
  {label, onClick, type="filled"}: 
  {
    label: string, 
    onClick: () => void,
    type?: "filled" | "outlined" | "outlined2"
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
    backgroundColor: c.primary,
    color: c.on_surface_white,
    fontWeight: "bold",
  },
  outlined: {
    border: `4px solid ${c.primary}`,
    color: c.primary
  },
  outlined2: {
    borderRadius: 32,
    border: '4px solid #9D20C9',
    color: "#fff",
    fontSize: "20px",
    padding: "8px 32px",
  }
}