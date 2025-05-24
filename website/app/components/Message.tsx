import { ProfileImage } from './';

/**
 * Komponent Message wyświetlający pojedynczą wiadomość
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.isUserAuthor - czy autorem wiadomości jest użytkownik (domyślnie false)
 * @param props.src - adres URL zdjęcia profilowego autora wiadomości
 * @param props.children - zawartość wiadomości
 * @param props.name - imię autora wiadomości (opcjonalne)
 * @param props.isFirst - czy jest to pierwsza wiadomość w grupie wiadomości (opcjonalne)
 * @param props.isLast - czy jest to ostatnia wiadomość w grupie wiadomości (opcjonalne)
 * @returns {JSX.Element} - komponent
 */
const Message = ({ isUserAuthor, src, children, name, isFirst, isLast }:{
  isFirst?: Boolean,
  isLast?: Boolean,
  name?: string
  isUserAuthor?: Boolean,
  src?: string,
  children: any
}) => (
  <div className={`flex-col gap-4 items-${isUserAuthor?"end":"start"}`}>
    {isFirst && 
      <div className={`justify-${isUserAuthor?"end":"start"}`}>{name}</div>
    }

    <div>
      <div 
        className={`justify-${isUserAuthor?"end":"start"} px-24 py-8 rounded-[16] msg white text-xl font-light`}
        style={isUserAuthor ? {borderEndEndRadius: 0} : {borderEndStartRadius: 0}}  
      >
        {children}
      </div>
    </div>

    {/* { isLast && src  
      && <ProfileImage src={src} size={24} /> 
    } */}
  </div>
)

export default Message