const Section = ({header, onClick, children}:{header: String,onClick?:()=>void, children: any}) => (
  <section className='flex-col grow gap-16' onClick={onClick}>
    <div className='text-[24px] font-bold on_bgc_primary'>{header}</div>
    {children}
  </section>
)

export default Section