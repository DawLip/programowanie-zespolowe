import c from '../colors';

/**
 * Komponent Divider wyświetlający poziomy lub pionowy pasek podziału
 * 
 * @param props - obiekt właściwości komponentu
 * @param props.color - kolor tła paska
 * @param props.vertical - jeśli true, pasek jest pionowy
 * @param props.horizontal - jeśli true, pasek jest poziomy
 * @returns {JSX.Element} - komponent
 */
export default function Divider(
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
