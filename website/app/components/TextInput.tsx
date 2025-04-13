import c from '../colors';

const Input = (
  {label, value, placeholder,password, setValue, long}:
  {
    label: string, 
    value: string, 
    placeholder:string, 
    password?: boolean,
    setValue: Function, 
    long?: boolean

  }) => (
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
            type={password ? "password" : "text"} 
            value={value}
            placeholder={placeholder}
            onChange={e=>setValue(e.target.value)}
            className={`flex on_surface_gray text-[32px]`}
          />
        )
    }
  </div>
)

export default Input;