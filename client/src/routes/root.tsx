import { useState} from "react";

export default function Root() {
  return (
    <>
      <div>
        <h1>Login or Register</h1>
        <p>you are not logged in</p>
        <a href={'/register'}><button>Register</button></a>
        <a href={'/login'}><button>Login</button></a>
      </div>
    </>
  );
}