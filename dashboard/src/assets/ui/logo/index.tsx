import Image from 'next/image'
import LogoImg from './logosm.png'
import React from 'react'

export default function Logo() {
  return (
    <Image
      src={LogoImg}
      width={98}
      height={100}
      alt="Company logo"
    />
  )
}
