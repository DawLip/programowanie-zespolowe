import c from '../colors';
export default function TextInput(
  {label, value, placeholder, password, setValue}: 
  {
    label: string, 
    value: string,
    placeholder?: string
    password?: boolean,
    setValue: Function
  }) {
  return (
    <div className="flex-col border-1 p-8 rounded-lg">
      <label className="text-xs on_surface_light_gray">{label}</label>
      <input 
        type={password ? "password" : "text"} 
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        className='text-xl'
      />
    </div>
  );
}
