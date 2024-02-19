import Link from 'next/link'

export default function Logo() {
  return (
    <Link href="/" className="block" aria-label="Cruip">
      <img src="/images/companycompasslogo.jpg" height="50" width="50"></img>
    </Link>
  )
}
