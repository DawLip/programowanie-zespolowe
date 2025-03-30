const ProfileImage = ({src, isActive, size}:{src: string, isActive?: Boolean, size: number}) => (
  <div className={`bg-black rounded-full items-end justify-end`} style={{width: size, height: size}}>
    {isActive && <div className={`bg-green-400 rounded-full size-16`}></div>}
  </div>
)

export default ProfileImage