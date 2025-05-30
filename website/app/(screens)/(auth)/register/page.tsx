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
 * Strona rejestracji użytkownika.
 * Zarządza formularzem rejestracji oraz przesyłaniem danych do API.
 * 
 * @returns {JSX.Element} Strona rejestracji.
 */
export default function LoginScreen() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [password, setPassword] = useState("");
  const [passwordR, setPasswordR] = useState("");

  useEffect(()=>{
    const token = Cookies.get('token');
    if (token) { router.push('/'); }
  },[])

  const onRegisterClick = () => {
    fetch(`${config.api}/auth/register`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, name, surname, password}), 
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
        <div className='justify-center text-[64px] font-bold on_surface_gray'>Register</div>
        <section className='flex-col gap-16 px-192'>
          <div className='flex-col gap-8'>
          <TextInput 
            value={email} 
            setValue={setEmail} 
            label="Email" 
            placeholder="excample@gmail.com"
          />
          <TextInput 
            value={name} 
            setValue={setName} 
            label="Name" 
            placeholder="Joe"
          />
          <TextInput 
            value={surname} 
            setValue={setSurname} 
            label="Surname" 
            placeholder="Doe"
          />
          <TextInput 
            value={password} 
            setValue={setPassword} 
            label="Password" 
            password
          />
          <TextInput 
            value={passwordR} 
            setValue={setPasswordR} 
            label="Retry password" 
            password
          />
          </div>
          <div className='flex-col gap-8'>
            <Button label="Register" onClick={onRegisterClick} type="filled"/>
          </div>
        </section>
      </div>
      
    <section className='flex-col on_surface_gray px-192'>
      <div className='justify-center'>Already have an account?</div>
      <Button label="Login" onClick={()=>router.push('/login')} type="outlined"/>
    </section>

     </section>
    </main>
  );
}
