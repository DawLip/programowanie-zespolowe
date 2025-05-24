"use client"

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation'
import Cookies from 'js-cookie';
import config from "../../../../config"

import {Header, Aside, Icon, Section, UserCard, Message, ProfileImage } from '../../../../components';

/**
 * Strona profilu użytkownika.
 * Umożliwia przeglądanie profili urzytkowników
 * 
 * @param {object} props - Właściwości komponentu
 * @param {{id: string}} props.params - Parametry trasy zawierające ID użytkownika
 * @returns {JSX.Element} Strona profilu użytkownika
 */
export default function Settings({params}: {params: {id: string}}) {
  const router = useRouter();

  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [about, setAbout] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [address, setAddress] = useState("");
  const [facebookURL, setFacebookURL] = useState("");
  const [instagramURL, setInstagramURL] = useState("");
  const [linkedinURL, setLinkedinURL] = useState("");

  useEffect(() => {
    fetch(`${config.api}/user/${params.id}`, {
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
  
  return (
    <>
      <Header header={"Profile"} backArrow />
      <main className='grow px-32'>
        <div className='flex-col grow gap-32 p-32 rounded-[32px] surface'>
          <div className='gap-16 items-center'>
            <ProfileImage src={""} size={64}/>
            <div className='gap-8'>
              <LineInput value={name} setValue={()=>{}} placeholder="Name"/>
              <LineInput value={surname} setValue={()=>{}} placeholder="Surname"/>
            </div>
          </div>
          <div className='flex-col gap-16'>
            <Input label={"About me"} value={about} placeholder={"Write something about you"} setValue={setAbout} long editable={false} />
            <Input label={"Email"} value={email} placeholder={"Your email"} setValue={setEmail} editable={false}/>
            <Input label={"Phone"} value={phone} placeholder={"Your phone number"} setValue={setPhone} editable={false} />
            <Input label={"Address"} value={address} placeholder={"Your address"} setValue={setAddress} editable={false} />
            <Input label={"Facebook URL"} value={facebookURL} placeholder={"Your facebook link"} setValue={setFacebookURL} editable={false} />
            <Input label={"Instagram URL"} value={instagramURL} placeholder={"Your instagram link"} setValue={setInstagramURL} editable={false} />
            <Input label={"LinkedInURL"} value={linkedinURL} placeholder={"Your LinkedIn link"} setValue={setLinkedinURL} editable={false} />
          </div>
        </div>
      </main>
    </>
  );
}

/**
 * Komponent wyświetlający jednoliniowy tekst (tylko do odczytu).
 * @param {object} props - Właściwości komponentu
 * @param {string} props.value - Wyświetlana wartość tekstowa
 * @param {string} props.placeholder - Tekst zastępczy wyświetlany, gdy wartość jest pusta
 * @param {Function} props.setValue - Funkcja ustawiająca wartość (nieużywana, bo komponent jest tylko do odczytu)
 * @returns {JSX.Element} JSX z tekstem wyświetlanym w divie
 */
export const LineInput = ({value, placeholder, setValue}:{value: string, placeholder: string, setValue: Function}) => {
  return (
    <div className='flex shrink text-5xl on_surface_gray'>
      {value}
    </div>
)}

/**
 * Komponent Input wyświetlający etykietę oraz pole tekstowe lub tekst tylko do odczytu.
 * @param {object} props - Właściwości komponentu
 * @param {string} props.label - Etykieta pola
 * @param {string} props.value - Wartość pola
 * @param {string} props.placeholder - Tekst zastępczy pola
 * @param {Function} props.setValue - Funkcja aktualizująca wartość
 * @param {boolean} [props.long] - Flaga czy pole ma być długie (textarea) czy jednolinijkowe (input)
 * @param {boolean} [props.editable] - Flaga czy pole jest edytowalne
 * @returns {JSX.Element} JSX z etykietą oraz odpowiednim polem (textarea/input lub span)
 */
export const Input = ({label, value, placeholder, setValue, long, editable}:{label: string, value: string, placeholder:string, setValue: Function, long?: boolean,editable?:boolean}) => (
  <div className='flex-col'>
    <span className='text-xl on_surface_light_gray font-bold'>{label}</span>
    {editable?`${
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
    }`
    : (
      long
        ? <span className='text-xl on_surface_gray font-bold'>{value}</span>
        : <span className='text-[32px] on_surface_gray font-bold'>{value}</span>
    )}
    
    
  </div>
)

