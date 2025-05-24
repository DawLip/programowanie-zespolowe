/**
 * Komponent ProfileImage wyświetlający okrągłe zdjęcie profilowe z oznaczeniem aktywności
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.src - adres URL zdjęcia profilowego
 * @param props.isActive - czy użytkownik jest aktywny (opcjonalne)
 * @param props.size - rozmiar obrazka (szerokość i wysokość w px)
 * @returns {JSX.Element} - komponent
 */
const ProfileImage = ({src, isActive, size}:{src: string, isActive?: Boolean, size: number}) => (
  <div 
    className={`bg-black rounded-full items-end justify-end`} 
    style={{
      width: size, height: size, 
      backgroundImage: `url(${src})`, 
      backgroundSize: 'cover', 
      backgroundPosition: 'center'
    }}>
    {isActive && <div className={`isActive rounded-full size-16`}></div>}
  </div>
)

export default ProfileImage