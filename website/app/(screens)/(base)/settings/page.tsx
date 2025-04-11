"use client"

import { useState, useRef, useEffect, use } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import config from "../../../config"

import {Header, Aside, Icon, Section, UserCard, Message, ProfileImage } from '../../../components';

export default function Settings() {
  const router = useRouter();

  const [name, setName] = useState("Adam");
  const [surname, setSurname] = useState("Freineg");
  const [about, setAbout] = useState("Za Twoją zgodą, my i nasi partnerzy (881) używamy plików cookie lub podobnych technologii do przechowywania i przetwarzania danych osobowych oraz uzyskiwania dostępu do tych danych, takich jak informacje o Twojej wizycie na tej stronie internetowej, adresy IP i identyfikatory plików cookie. Niektórzy partnerzy nie proszą o zgodę");
  const [email, setEmail] = useState("+48 505 575 832");
  const [phone, setPhone] = useState("Katowice, Krakowska 73a");
  const [address, setAddress] = useState("fdsafdsfdg fd ");
  const [facebookURL, setFacebookURL] = useState("gfdsgdfsgdfs");
  const [instagramURL, setInstagramURL] = useState("gfdsgsdfgdfs");
  const [linkedinURL, setLinkedinURL] = useState("gfdsgfdsg");

  const userID = Cookies.get('userId')
    
  useEffect(() => {
    fetch(`${config.api}/user/${userID}`, {
      headers: {"Authorization": `Bearer ${Cookies.get('token')}`}
    })
      .then(response => response.json())
      .then((response:any) => {
        setName(response.name || "");
        setSurname(response.surname || "");
        setAbout(response.about || "");
        setEmail(response.email || "");
        setPhone(response.phone || "");
        setAddress(response.address || "");
        setFacebookURL(response.facebookURL || "");
        setInstagramURL(response.instagramURL || "");
        setLinkedinURL(response.linkedinURL || "");
      })
      .catch(error => console.error('Błąd:', error));
  }, [])

  const handleSave = () => {
    fetch(`${config.api}/user/${userID}`, {
      method: 'POST',
      headers: {
        "Authorization": `Bearer ${Cookies.get('token')}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name,
        surname,
        about,
        email,
        phone,
        address,
        facebook: facebookURL,
        instagram: instagramURL,
        linkedin: linkedinURL
      })
    })
      .then(response => response.json())
      .then((response:any) => {
        console.log(response);
      })
      .catch(error => console.error('Błąd:', error));
  }
  
  return (
    <>
    <Header header={"Profile"} name={"Adam"} surname={"Freineg"} backArrow />
    <main className='grow px-32'>
      <div className='flex-col grow gap-32 p-32 rounded-[32px] surface'>
        <div className='gap-16 items-center'>
          <ProfileImage src={""} size={64}/>
          <div>
            <LineInput value={name} setValue={setName} placeholder="Name"/>
            <LineInput value={surname} setValue={setSurname} placeholder="Surname"/>
          </div>
          <div className='px-16 py-8 bg-amber-50 rounded-full' onClick={handleSave}>Save</div>
        </div>
        <div className='flex-col gap-16'>
          <Input label={"About me"} value={about} placeholder={"Write something about you"} setValue={setAbout} long />
          <Input label={"Email"} value={email} placeholder={"Your email"} setValue={setEmail}/>
          <Input label={"Phone"} value={phone} placeholder={"Your phone number"} setValue={setPhone} />
          <Input label={"Address"} value={address} placeholder={"Your address"} setValue={setAddress} />
          <Input label={"Facebook URL"} value={facebookURL} placeholder={"Your facebook link"} setValue={setFacebookURL} />
          <Input label={"Instagram URL"} value={instagramURL} placeholder={"Your instagram link"} setValue={setInstagramURL} />
          <Input label={"LinkedIn URL"} value={linkedinURL} placeholder={"Your LinkedIn link"} setValue={setLinkedinURL} />
        </div>
      </div>
    </main>
    </>
  );
}

const LineInput = ({value, placeholder, setValue}:{value: string, placeholder: string, setValue: Function}) => {
  const spanRef = useRef<HTMLSpanElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => { if (spanRef.current && inputRef.current) inputRef.current.style.width = `${spanRef.current.offsetWidth + 10}px`; }, [value]);

  return (
  <>
    <input 
      type="text" 
      ref={inputRef}
      value={value} 
      onChange={e=>setValue(e.target.value)} 
      placeholder="Name"
      className='flex shrink text-5xl on_surface_gray'
      style={{ width: `${value.length}ch` }}
    />
    <span ref={spanRef} className="absolute invisible text-5xl">{value || placeholder}</span>
  </>
)}

const Input = ({label, value, placeholder, setValue, long}:{label: string, value: string, placeholder:string, setValue: Function, long?: boolean}) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    {
      long
        ? (
          <textarea 
            value={value} 
            placeholder={placeholder} 
            onChange={e=>setValue(e.target.value)}
            className={`flex on_surface_gray text-xl`}
          />
        )
        : (
          <input 
            type="text" 
            value={value}
            placeholder={placeholder}
            onChange={e=>setValue(e.target.value)}
            className={`flex on_surface_gray text-[32px]`}
          />
        )
    }
    
    
  </div>
)

