const Section = ({header, children}:{header: String, children: any}) => (
  <section className='flex-col grow gap-16'>
    <div className='text-[24px] font-bold on_surface_light_gray'>{header}</div>
    {children}
  </section>
)

export default Section