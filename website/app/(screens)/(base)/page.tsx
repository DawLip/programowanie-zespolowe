"use client"
import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import { useSocket } from '../../socket';
import config from "./../../config"

import {Header, Aside, Icon, Section, UserCard, Message } from './../../components/';

export default function Home() {
  const router = useRouter();
  const { socket, isConnected } = useSocket();

  const [user, setUser] = useState<any>({});

  const [users, setUsers] = useState<any[]>([]);
  const [groups, setGroups] = useState<any[]>([]);
  const [mayKnow, setMayKnow] = useState<any[]>([]);
  const [invitations, setInvitations] = useState<any[]>([]);

  const userId = Cookies.get('userId');

  const updateDashboard = () => {
    fetch(`${config.api}/dashboard`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log("/dashboard", response)

        setUsers(response.lastChats);
        setGroups(response.groups)
        setMayKnow(response.mayKnow)
        setInvitations(response.invitations)
      })
      .catch(error => console.error('Błąd:', error));

      fetch(`${config.api}/user/${userId}`, {
        headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
      })
        .then(response => response.json())
        .then((response:any) => {
          console.log("${config.api}/user/${userId", response)
          setUser(response);
        })
        .catch(error => console.error('Błąd:', error));
  }
  useEffect(() => updateDashboard(), [])

  useEffect(() => {
      if(!isConnected) return;
      socket.on("new_message", (message:any) => {
        updateDashboard()
      });
    }, [socket, isConnected]);

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
    setInvitations(prev=>prev.filter(inv => inv!=friend_id))

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
      <Header header={`Welcome ${user.name}`}/>
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
                key={"d-f"+u.id}
                name={u.name} 
                surname={u.surname} 
                isActive={u.isActive}
                onClickCard={()=>router.push(`/chat/private/${u.roomId}`)}
              >
                <div className='flex-col gap-8 pt-8'>
                  {u.messages?.map((m:any, i:number) => (
                    <Message key={i} isUserAuthor={m.userId == userId}>{m.message}</Message>
                  ))}
                </div>
              </UserCard>
            ))}
          </div>
        </Section>
        <Section header="Groups">
          <div className='flex-wrap gap-16 items-stretch'>
            {groups && groups.map(g => (
              <UserCard 
                key={"dg"+g.groupId}
                name={g.name} 
                surname="" 
                isActive={g.isActive}
                onClickCard={()=>router.push(`/chat/group/${g.roomId}`)}
              >
                <div className='flex-col grow-999 gap-8 pt-8 justify-end'>
                  { g.messages?.map((m:any, i:number) => (
                    <Message key={i+m.message} isUserAuthor={m.userId == userId}>{m.message}</Message>
                  ))}
                </div>
              </UserCard>
            ))}
          </div>
        </Section>
        <Section header="You may know">
            <div className='flex-wrap gap-16'>
              {mayKnow && mayKnow.map((mn)=><UserCard 
                key={"d-mn"+mn.id}
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


