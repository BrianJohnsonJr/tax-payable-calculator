import { useState } from 'react'
import './App.css'

type LineItem = {description: string; category: string; amount: string; tax_rate: string; tax_amount: string; vendor: string}
type Invoice = { invoiceId: string; vendor: string; status: string; tax_applied: boolean; total_tax: string; override_reason: string | null; line_items: LineItem[] }
const API = "https://fmskteyovd.execute-api.us-east-1.amazonaws.com/Prod"

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [invoice, setInvoice] = useState<Invoice | null>(null)
  const [status, setStatus] = useState<string>("idle")

  return (
    <>
      <h1>Invoice Tax Calculator </h1>
      <input type="file" onChange={e=> setFile(e.target.files?.[0] ?? null)}/>
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <p>{status}</p>
    </>
  )
}
export default App
