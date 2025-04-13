"use client"

import React, { useState, useRef, useEffect, createContext, useContext } from 'react';
import { useRouter } from 'next/navigation'
import { SocketProvider, useSocket } from '../../socket';
import Cookies from 'js-cookie';
import config from "../../config"

import {Header, Aside, Icon, Section, UserCard, Message, ProfileImage } from '../../components';

export default function Layout({children}: {children: any}) {
  const router = useRouter();

  const userID = Cookies.get('userId')
  const [users, setUsers] = useState<any[]>([]);
  const [groups, setGroups] = useState<any[]>([]);
  const { socket, isConnected } = useSocket();

  useEffect(() => { if(!Cookies.get('token')) router.push('/login') },[] )
    
  useEffect(() => {
    fetch(`${config.api}/aside`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("response", response)

        setUsers(response.friends);
        setGroups(response.groups)
      })
      .catch(error => console.error('Błąd:', error));
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