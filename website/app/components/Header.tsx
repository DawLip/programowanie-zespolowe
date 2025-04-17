"use client"
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import config from '../config';

import { Divider, Icon, ProfileImage } from './';

import c from '../colors';
import { use } from 'react';

const Header =(
  {header, backArrow, userProfileSrc}: 
  {
    header: any, 
    backArrow?: boolean,
    userProfileSrc?: string
  }) => {
  const router = useRouter();

  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");


  const logout = () => {
    Cookies.remove('token');
    router.push('/login');
  }

  const userID = Cookies.get('userId')
  useEffect(() => {
    fetch(`${config.api}/user/${userID}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        setName(response.name || "");
        setSurname(response.surname || "");
      })
      .catch(error => console.error('Błąd:', error));
  },[])
  
  return (
    <header className='justify-between px-32 h-96'>
      <div className='items-center gap-16 text-[32px] on_surface_gray font-bold'>
        {backArrow && <Icon src={"/icons/back-arrow.png"} size={40} onClick={()=>router.back()}/>}
        {userProfileSrc && <ProfileImage src={userProfileSrc} size={40} isActive={true}/>}
        {header}
      </div>
      <div className='gap-24 py-24'>
        <div className='items-center gap-12 cursor-pointer' onClick={()=>router.push('/settings')}>
          <span className='text-[24px] on_surface_light_gray'>{name} {surname}</span>
          <ProfileImage src={""} size={32} />
        </div>
        <Divider color={"#7B7B7B"} vertical />
        <div className='items-center gap-16'>
          <Icon src={"/icons/settings.png"} size={32} onClick={()=>router.push('/settings')} />
          <Icon src={"/icons/logout.png"} size={32} onClick={logout} />
        </div>
      </div>
    </header>
  );
}

export default Header