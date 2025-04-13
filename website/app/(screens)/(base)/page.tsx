"use client"
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import config from "./../../config"

import {Header, Aside, Icon, Section, UserCard, Message } from './../../components/';

export default function Home() {
  const router = useRouter();

  const [users, setUsers] = useState<any[]>([]);
  const [groups, setGroups] = useState<any[]>([]);
  const [mayKnow, setMayKnow] = useState<any[]>([]);
  const [invitations, setInvitations] = useState<any[]>([]);

  useEffect(() => { if(!Cookies.get('token')) router.push('/login') },[] )
  useEffect(() => {
    fetch(`${config.api}/dashboard`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("response", response)

        setUsers(response.users);
        setGroups(response.groups)
        setMayKnow(response.mayKnow)
        setInvitations(response.invitations)
      })
      .catch(error => console.error('Błąd:', error));
  }, [])

  const inviteFriend = (friend_id:number) => {
    fetch(`${config.api}/user/invite/${friend_id}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`},
      method: "POST",
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("response", response)
      })
      .catch(error => console.error('Błąd:', error));
  }
  const handleInvitation = (friend_id:number, method:string) => {
    fetch(`${config.api}/user/invitation-${method}/${friend_id}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`},
      method: "POST",
    })
      .then(response => response.json())
      .then((response:any) => {console.log("response", response)})
      .catch(error => console.error('Błąd:', error));
  }
  
  return (
    <>
      <Header header={"Welcome Adam"}/>
      <main className='flex-col grow gap-32 px-32'>
        {invitations && invitations[0] && <Section header="Invitations">
          {invitations.map(invitation => (
          <UserCard 
            name={invitation.name}
            surname={invitation.surname}
            isActive={true} 
            buttons={
              <>
                <Icon src={"/icons/cross.png"} size={24} onClick={()=>{handleInvitation(invitation.id, "decline")}}/>
                <Icon src={"/icons/check.png"} size={32} onClick={()=>{handleInvitation(invitation.id, "accept")}}/>
              </>
            }
          />))}
        </Section>}
        <Section header="Friends">
          <div className='flex-wrap gap-32'>
            {users && users.map(u => (
              <UserCard 
                key={u.id}
                name={u.name} 
                surname={u.surname} 
                isActive={u.isActive}
                onClick={()=>router.push('/chat')}
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
          <div className='flex-wrap gap-16 items-stretch'>
            {groups && groups.map(g => (
              <UserCard 
                key={g.groupId}
                name={g.name} 
                surname="" 
                isActive={g.isActive}
                onClick={()=>router.push('/chat')}
              >
                <div className='flex-col grow-999 gap-8 pt-8 justify-end'>
                  { g.messages?.map((m:any, i:number) => (
                    <Message key={i} isUserAuthor={m.authorId == 0}>{m.message}</Message>
                  ))}
                </div>
              </UserCard>
            ))}
          </div>
        </Section>
        <Section header="You may know">
            <div className='flex-wrap gap-16'>
              {mayKnow && mayKnow.map((mn)=><UserCard 
                name={mn.name}
                surname={mn.surname} 
                isActive={mn.isActive} 
                buttons={<Icon src="/icons/add-friend.png" size={24} onClick={()=>inviteFriend(mn.id)}/>}
                onClick={()=>router.push(`/profile/${mn.id}`)}
              />)}
            </div>
        </Section>
      </main>
    </>
  );
}


