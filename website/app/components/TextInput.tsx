import c from '../colors';

/**
 * Komponent Input wyświetlający pole do wprowadzania textu z etykietą
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.label - etykieta pola
 * @param props.value - aktualna wartość pola
 * @param props.placeholder - tekst zastępczy w polu (opcjonalny)
 * @param props.password - czy pole jest typu hasło (opcjonalne)
 * @param props.setValue - funkcja ustawiająca nową wartość pola
 * @param props.long - czy użyć pola textarea zamiast input (opcjonalne)
 * @returns {JSX.Element} - komponent
 */
const Input = (
  {label, value, placeholder,password, setValue, long}:
  {
    label: string, 
    value: string, 
    placeholder?:string, 
    password?: boolean,
    setValue: Function, 
    long?: boolean

  }) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    {
      long
        ? (
          <textarea 
            value={value} 
            placeholder={placeholder} 
            onChange={e=>setValue(e.target.value)}
            className={`flex on_surface_gray text-xl`}
          />
        )
        : (
          <input 
            type={password ? "password" : "text"} 
            value={value}
            placeholder={placeholder}
            onChange={e=>setValue(e.target.value)}
            className={`flex on_surface_gray text-[32px]`}
          />
        )
    }
  </div>
)

export default Input;