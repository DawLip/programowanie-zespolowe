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