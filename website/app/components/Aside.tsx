"use client"

import { useState } from 'react'
import { useRouter } from 'next/navigation'

import { ProfileImage, Button } from './'

import c from '../colors'

export default function Aside({ users, groups }:{users: any, groups: any}) {
  const [friendsOrGroups, setFriendsOrGroups] = useState(true)
  const router = useRouter();

  return (
    <aside className="sticky top-0 w-256 h-screen flex-col gap-16 p-16 aside_bg">
      <header className="white text-3xl font-bold justify-center">
        ChatNow
      </header>
      <section className="flex-col gap-16">
        <div>
          <FriendsGroupButton label ="Friends" callback={setFriendsOrGroups} checked={friendsOrGroups}/>
          <FriendsGroupButton label ="Groups" callback={setFriendsOrGroups} checked={!friendsOrGroups}/>
        </div>
        <div 
          className="flex-col overflow-y-scroll scrollbar-none gap-16" 
          style={{height: "calc(100vh - 124px - 16px)"}}
        >
          {!friendsOrGroups && <Button label="Create" onClick={()=>router.push("/group-settings")} type="outlined2" />}
          {users.map((u:any) => <UserCard user={u} onClick={()=>router.push("/chat")}/>)}
        </div>
      </section>
    </aside>
  );
}

const UserCard = ({user, onClick}:{user: any, onClick?: () => void}) => (
  <div className="gap-8 w-256" onClick={onClick}>
    <ProfileImage src={""} size={40} isActive={user.isActive} />
    <div className={`flex-col gap-4 text-base/19 ${onClick && "hover:cursor-pointer"}`}>
      <div className="on_nav font-semibold">
        {user.name} {user.surname}
      </div>
      <div className="on_nav">
        {user.lastMessageAuthor} {user.lastMessage}
      </div>
    </div>
  </div>
)

function FriendsGroupButton({callback, label, checked}:{callback: Function, label: string, checked: boolean}){
  return (
    <button 
      onClick={()=>callback(label==="Friends")} 
      className={`grow on_nav py-8 ${checked && `border-b-1 border-[${c.border}]`} font-bold`}
      style={{borderBottom: checked?`1px solid rgba(247, 231, 253, 0.80)`:`1px solid rgba(0, 0, 0, 0)`}}
    >
      {label}
    </button>
  )
}