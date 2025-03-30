"use client"
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';

import TextInput from "../../components/TextInput";
import Button from "../../components/Button";

export default function LoginScreen() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [password, setPassword] = useState("");
  const [passwordR, setPasswordR] = useState("");

  useEffect(()=>{
    const token = Cookies.get('token');
    if (token) {
      router.push('/');
    }
  },[])

  return (
    <main className="min-h-screen">
     <section className="flex-1 px-192 py-128 bg-gray-200"></section>
     <section className="flex-1 flex-col min-h-screen px-192 py-128 justify-between on_surface_gray">
      
      <div className='justify-center text-8xl font-bold'>Register</div>

      <section className='flex-col gap-16'>
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
          <Button label="Register" onClick={()=>{}} type="filled"/>
        </div>
      </section>
      
    <section className='flex-col on_surface_gray'>
      <div className='justify-center'>Already have an account?</div>
      <Button label="Login" onClick={()=>{}} type="outlined"/>
    </section>

     </section>
    </main>
  );
}
