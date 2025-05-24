import { ProfileImage } from './'

/**
 * Komponent UserCard wyświetlający kartę użytkownika
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.name - imię użytkownika
 * @param props.surname - nazwisko użytkownika
 * @param props.isActive - czy użytkownik jest aktywny
 * @param props.buttons - opcjonalne przyciski do wyświetlenia obok nazwy (opcjonalne)
 * @param props.children - kontent karty (opcjonalne)
 * @param props.style - dodatkowe stylowanie (opcjonalne)
 * @param props.className - klasy (opcjonalne)
 * @param props.onClick - funkcja wywoływana po kliknięciu na element z imieniem i nazwiskiem (opcjonalne)
 * @param props.onClickCard - funkcja wywoływana po kliknięciu na całą kartę (opcjonalne)
 * @returns {JSX.Element} - komponent
 */
const UserCard = ({name, surname, isActive, buttons, children, style, className, onClick, onClickCard}:{
  name: String,
  surname: String,
  isActive: Boolean,
  buttons?: any,
  children?: any,
  style?: any,
  className?:string,
  onClick?: () => void,
  onClickCard?: () => void
}) => (
  <div 
    className={`flex-col grow rounded-[32] surface min-w-400 ${className} ${onClickCard && "hover:cursor-pointer"}`} 
    style={{padding: children ? 32 : 16, ...style}}
    onClick={onClickCard}
  >
    <header className={`grow justify-between`} >
      <div className={`gap-16 items-center ${onClick && "hover:cursor-pointer"}`} onClick={onClick}>
        <ProfileImage src={""} isActive={isActive} size={40}/>
        <span className='text-[24px] font-semibold on_surface_gray'>{name} {surname}</span>
      </div>
      {buttons && <div className='gap-24 items-center pr-8'>{buttons}</div>}
    </header>
    {children}
  </div>
)

export default UserCard