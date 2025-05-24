/**
 * Komponent Section wyświetlający sekcję z nagłówkiem i zawartością
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.header - nazwa sekcji
 * @param props.onClick - funkcja wywoływana po kliknięciu na sekcję (opcjonalne)
 * @param props.children - zawartość sekcji
 * @returns {JSX.Element} - komponent
 */
const Section = ({header, onClick, children}:{header: String,onClick?:()=>void, children: any}) => (
  <section className='flex-col grow gap-16' onClick={onClick}>
    <div className='text-[24px] font-bold on_bgc_primary'>{header}</div>
    {children}
  </section>
)

export default Section