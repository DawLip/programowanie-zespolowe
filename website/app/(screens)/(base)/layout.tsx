"use client"

import { useState, useRef, useEffect, use } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import config from "../../config"

import {Header, Aside, Icon, Section, UserCard, Message, ProfileImage } from '../../components';

export default function Layout({children}: {children: React.ReactNode}) {
  const router = useRouter();

  const userID = Cookies.get('userId')
  
  const u = { id: 0, name: 'John', surname:'Doe', lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const g = { id: 0, name: "Python lovers", lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const users = [u,u,u];
  const groups = [g,g,g];


  useEffect(() => { if(!Cookies.get('token')) router.push('/login') },[] )
    
  useEffect(() => {

    // fetch(`${config.api}/user/${userID}`, {
    //   headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    // })
    //   .then(response => response.json())
    //   .then((response:any) => {
    //   })
    //   .catch(error => console.error('Błąd:', error));
  }, [])

  
  return (
    <main className='grow'>
      <Aside users={users} groups={groups} />
      <div className='flex-col grow pb-32'>
      {children}
      </div>
    </main>
  );
}

