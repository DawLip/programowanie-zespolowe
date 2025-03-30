"use client"

import { useState } from 'react'
import { ProfileImage } from './'

import c from '../colors'

export default function Aside({ users, groups }:{users: any, groups: any}) {
  const [friendsOrGroups, setFriendsOrGroups] = useState(true)
  return (
    <aside className="sticky top-0 w-256 h-screen flex-col gap-16 p-16 surface">
      <header className="on_surface_gray text-3xl font-bold justify-center">
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
          {users.map((u:any) => (<UserCard user={u}/>))}
        </div>
      </section>
    </aside>
  );
}

function UserCard({user}:{user: any}){
  return (
    <div className="gap-8 w-256">
      <ProfileImage src={""} size={40} isActive={user.isActive} />
      <div className="flex-col gap-4 text-base/19">
        <div className="on_surface_gray font-semibold">
          {user.name} {user.surname}
        </div>
        <div className="on_surface_light_gray">
          {user.lastMessageAuthor} {user.lastMessage}
        </div>
      </div>
    </div>
  )
}

function FriendsGroupButton({callback, label, checked}:{callback: Function, label: string, checked: boolean}){
  return (
    <button 
      onClick={()=>callback(label==="Friends")} 
      className={`grow on_surface_gray py-8 ${checked && `border-b-1 border-[${c.border}]`}`}
    >
      {label}
    </button>
  )
}