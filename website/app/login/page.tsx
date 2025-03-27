"use client"
import { useState } from 'react'

import TextInput from "../components/TextInput";
import Button from "../components/Button";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

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
          <Button label="Login" onClick={()=>{}} type="filled"/>
          <div className='gap-8 justify-center'>
            <span className='on_surface_gray'>Do you forgot password?</span> 
            <a href="/reset-password"><span className='font-bold'>Reset password</span></a>
          </div>
        </div>
      </section>
      
    <section className='flex-col on_surface_gray'>
      <div className='justify-center'>Don't have an account yet?</div>
      <Button label="Register" onClick={()=>{}} type="outlined"/>
    </section>

     </section>
    </main>
  );
}
