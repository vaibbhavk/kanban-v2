// export default async function checkAuthToken() {
//   if (localStorage.getItem("token")) {
//     // check whether the auth token is valid
//     const result = await fetch(
//       "http://localhost:5000/api/user/check_auth_token",
//       {
//         method: "GET",
//         headers: {
//           Authorization: "Bearer " + localStorage.getItem("token"),
//         },
//       }
//     );
//     if (result.status === 200) return true;
//   }
//   return false;
// }
export default function checkAuthToken() {
  if (localStorage.getItem("token")) return true;
  return false;
}
