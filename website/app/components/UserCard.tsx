import { ProfileImage } from './'

const UserCard = ({name, surname, isActive, buttons, children}:{
  name: String,
  surname: String,
  isActive: Boolean,
  buttons?: any,
  children?: any
}) => (
  <div 
    className='flex-col grow rounded-[32] surface min-w-400' 
    style={{padding: children ? 32 : 16}}
  >
    <header className='grow justify-between'>
      <div className='gap-16 items-center'>
        <ProfileImage src={""} isActive={isActive} size={40}/>
        <span className='text-[24px] font-semibold on_surface_gray'>{name} {surname}</span>
      </div>
      {buttons && <div className='gap-24 items-center pr-8'>{buttons}</div>}
    </header>
    {children}
  </div>
)

export default UserCard