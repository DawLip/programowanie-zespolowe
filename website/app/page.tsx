"use client"
import { useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import {Header, Aside, Icon, Section, UserCard, Message } from './components/';

export default function Home() {
  const router = useRouter();
  
  const u = { id: 0, name: 'John', surname:'Doe', lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const g = { id: 0, name: "Python lovers", lastMessage: "hey!", lastMessageAuthor:"you", isActive: true }
  const users = [u,u,u,u,u,u];
  const groups = [g,g,g,g,g];

  useEffect(() => { if(!Cookies.get('token')) router.push('/login') },[] )
  
  return (
    <main className='grow'>
      <Aside users={users} groups={groups} />
      <div className='flex-col grow pb-32'>
        <Header header={"Welcome Adam"} name={"Adam"} surname={"Freineg"} />
        <main className='flex-col grow gap-32 px-32'>
          <Section header="Invitations">
            <UserCard 
              name="John" 
              surname="Doe" 
              isActive={true} 
              buttons={
              <>
                <Icon src={"/icons/cross.png"} size={24} onClick={()=>{}}/>
                <Icon src={"/icons/check.png"} size={24} onClick={()=>{}}/>
              </>
              }
            />
          </Section>
          <Section header="Friends">
            <div className='flex-wrap gap-32'>
              {users.map(u => (
                <UserCard 
                  key={u.id}
                  name={u.name} 
                  surname={u.surname} 
                  isActive={u.isActive}
                >
                  <div className='flex-col gap-8'>
                    <Message isUserAuthor={true}>Hey, whats up?</Message>
                    <Message isUserAuthor={false}>Hey, whats up?</Message>
                    <Message isUserAuthor={true}>Hey, whats up?</Message>
                  </div>
                </UserCard>
              ))}
            </div>
          </Section>
          <Section header="Groups">
            <div className='flex-wrap gap-16'>
              {groups.map(g => (
                <UserCard 
                  key={g.id}
                  name={g.name} 
                  surname="" 
                  isActive={g.isActive}
                >
                  <div className='flex-col gap-8'>
                    <Message isUserAuthor={true}>Hey, whats up?</Message>
                    <Message isUserAuthor={false}>Hey, whats up?</Message>
                    <Message isUserAuthor={true}>Hey, whats up?</Message>
                  </div>
                </UserCard>
              ))}
            </div>
          </Section>
          <Section header="You may know">
              <div className='flex-wrap gap-16'>
                {[0,1,2,3,4,5,6,7,8,9,10,11].map(()=><UserCard 
                  name="John" 
                  surname="Doe" 
                  isActive={true} 
                  buttons={<Icon src="/icons/add-friend.png" size={32} onClick={()=>{}}/>}
                />)}
              </div>
          </Section>
        </main>
      </div>
    </main>
  );
}


