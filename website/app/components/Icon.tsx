"use Client"

/**
 * Komponent Icon wyświetlający ikonę
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.src - źródło obrazka (jeśli pusty, wyświetlany jest obraz domyślny)
 * @param props.size - rozmiar ikony
 * @param props.onClick - funkcja wywoływana po kliknięciu na ikonę
 * @returns {JSX.Element} - komponent
 */
const Icon = ({src, size, onClick}:{src?: string, size: number, onClick: ()=>void}) => (
  <img 
    src={src==""?"/placeholder.png":src} 
    style={{height:size, width: size}} 
    className="hover:cursor-pointer"
    onClick={onClick}
  />
)

export default Icon