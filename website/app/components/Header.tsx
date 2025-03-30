import { Divider, Icon, ProfileImage } from './';

import c from '../colors';

const Header =(
  {header, name, surname, backArrow}: 
  {
    header: string, 
    name: string,
    surname: string,
    backArrow?: boolean,
  }) => {
  return (
    <header className='justify-between px-32 h-96'>
      <div className='items-center text-[32px] on_surface_gray font-bold'>
        {backArrow && <Icon src={""} size={40} onClick={()=>{}}/>}
        {header}
      </div>
      <div className='gap-24 py-24'>
        <div className='items-center gap-12'>
          <span className='text-[24px] on_surface_light_gray'>{name} {surname}</span>
          <ProfileImage src={""} size={32} />
        </div>
        <Divider color={"#7B7B7B"} vertical />
        <div className='items-center gap-16'>
          <Icon src={"/icons/settings.png"} size={32} onClick={()=>{}} />
          <Icon src={"/icons/logout.png"} size={32} onClick={()=>{}} />
        </div>
      </div>
    </header>
  );
}

export default Header