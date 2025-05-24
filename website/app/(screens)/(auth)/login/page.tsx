"use client"
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import TextInput from "../../../components/TextInput";
import Button from "../../../components/Button";
import UserCard from "../../../components/UserCard";
import Message from "../../../components/Message";

import config from "../../../config"

/**
 * Strona logowania.
 * Zarządza formularzem logowania użytkownika.
 * 
 * @returns {JSX.Element} Strona logowania.
 */
export default function LoginScreen() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onLoginClick = () => {
    fetch(`${config.api}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password}), 
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log(response)
        if (response.access_token) {
          Cookies.set('token', response.access_token);
          Cookies.set('userId', response.userId);
          router.push('/');
        }
      })
      .catch(error => console.error('Błąd:', error));
  }

  useEffect(()=>{
    const token = Cookies.get('token');
    if (token) {
      router.push('/');
    }
  },[])

  return (
    <main className="min-h-screen bgc">
     <section className="flex-1 flex-col gap-64 login_bg justify-center items-center"> 
      <div className='white font-bold text-[64px]'>Stay in touch...</div>
      <div className='w-656 h-436' style={{display: 'block', position: 'relative'}}>
        <UserCard name={"John"} surname={"Brown"} isActive={true} style={{position: "absolute", left: 0, top: 0, width: 256}} className="login_cards_shadow">
          <div className='flex-col gap-8 pt-8'>
              <Message isUserAuthor={false}>Hey</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={false}>Wanna</Message>
            </div>
        </UserCard>
        <UserCard name={"Annie"} surname={"Blau"} isActive={true} style={{position: "absolute", left: 128, top: 64, width: 256}} className="login_cards_shadow">
          <div className='flex-col gap-8 pt-8'>
          <Message isUserAuthor={false}>What about</Message>
              <Message isUserAuthor={true}>Hey, whats up?</Message>
              <Message isUserAuthor={false}>Can you?</Message>
            </div>
        </UserCard>
        <UserCard name={"Robert"} surname={"Kraus"} isActive={true} style={{position: "absolute", left: 256, top: 128, width: 256}} className="login_cards_shadow" >
          <div className='flex-col gap-8 pt-8'>
          <Message isUserAuthor={false}>Hey, whats up?</Message>
              <Message isUserAuthor={true}>Coffe?</Message>
              <Message isUserAuthor={false}>Coffe :D</Message>
            </div>
        </UserCard>
      </div>
      <div className='white font-bold text-[64px]'>...with your friends</div>
     </section>

     <section className="flex-1 flex-col min-h-screen pb-64 pt-16 justify-between on_surface_gray">
      <div className='justify-center text-[84px] font-bold on_bgc_primary'>ChatNow</div>
      <div className='flex-col gap-32'>
        <div className='justify-center text-[64px] font-bold on_surface_gray'>Login</div>
        <section className='flex-col gap-16 px-192'>
          <div className='flex-col gap-8'>
            <TextInput 
              value={email} 
              setValue={setEmail} 
              label="Email" 
              placeholder="excample@gmail.com"
            />
            <TextInput 
              value={password} 
              setValue={setPassword} 
              label="Password" 
              password
            />
          </div>
          <div className='flex-col gap-8'>
            <Button label="Login" onClick={onLoginClick} type="filled"/>
            <div className='gap-8 justify-center'>
              <span className='on_surface_gray'>Do you forgot password?</span> 
              <a href="/reset-password"><span className='font-bold on_bgc_primary'>Reset password</span></a>
            </div>
          </div>
        </section>
      </div>
      
    <section className='flex-col on_surface_gray px-192'>
      <div className='justify-center'>Don't have an account yet?</div>
      <Button label="Register" onClick={()=>router.push('/register')} type="outlined"/>
    </section>

     </section>
    </main>
  );
}
