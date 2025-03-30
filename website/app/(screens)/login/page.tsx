"use client"
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import TextInput from "../../components/TextInput";
import Button from "../../components/Button";

import config from "../../config"

export default function LoginScreen() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onLoginClick = () => {
    fetch(`http://localhost:3001/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password}), 
    })
      .then(response => response.json())
      .then(data => console.log('Sukces:', data))
      .catch(error => console.error('Błąd:', error));
    // Cookies.set('user', 'JohnDoe', { expires: 7 })
  }

  return (
    <main className="min-h-screen">
     <section className="flex-1 px-192 py-128 bg-gray-200"></section>
     <section className="flex-1 flex-col min-h-screen px-192 py-128 justify-between on_surface_gray">
      
      <div className='justify-center text-8xl font-bold'>Sign in</div>

      <section className='flex-col gap-16'>
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
            <a href="/reset-password"><span className='font-bold'>Reset password</span></a>
          </div>
        </div>
      </section>
      
    <section className='flex-col on_surface_gray'>
      <div className='justify-center'>Don't have an account yet?</div>
      <Button label="Register" onClick={()=>router.push('/register')} type="outlined"/>
    </section>

     </section>
    </main>
  );
}
