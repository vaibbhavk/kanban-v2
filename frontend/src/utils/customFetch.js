export default async function customFetch(url, init_obj, response_type = "j") {
  let res = null;
  let data = null;
  try {
    res = await fetch(url, init_obj);
  } catch {
    throw new Error("Network error occured");
  }
  try {
    if (response_type === "j") data = await res.json();
    else if (response_type === "b") data = await res.blob();
  } catch {
    throw new Error("Response body was not json or blob");
  }
  if (res.status === 200 || res.status === 201) {
    return data;
  } else {
    throw new Error(data.error_message);
  }
}
