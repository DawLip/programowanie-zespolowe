import c from '../colors';
export default function Header(
  {color, vertical, horizontal}: 
  {
    color: string, 
    vertical?: boolean, 
    horizontal?: boolean, 
  }) {
  const h = horizontal && "h-1"
  const v = vertical && "w-1"
  return (
    <div className={`grow ${h} ${v} rounded-full`} style={{backgroundColor: c.border}}></div>
  );
}
