import { useState } from 'react'
import './App.css'

type LineItem = {description: string; category: string; amount: string; tax_rate: string; tax_amount: string}
type Invoice = { invoiceId: string; vendor: string; status: string; tax_applied: boolean; total_tax: string; override_reason: string | null; line_items: LineItem[] }
const API = "https://fmskteyovd.execute-api.us-east-1.amazonaws.com/Prod"

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [invoice, setInvoice] = useState<Invoice | null>(null)
  const [status, setStatus] = useState<string>("idle")

  async function pollForInvoice(key: string): Promise<Invoice>{
    for (let i = 0; i < 20; i++){
      const res = await fetch(`${API}/invoices`)
      const invoices: Invoice[] = await res.json()

      const match = invoices.find(inv => inv.invoiceId === key)
      if (match){
        return match
      }
      await new Promise(r => setTimeout(r, 2000))
    }
    throw new Error("timed out")
  }

  async function handleUpload(){
    if (!file) return
    try{
      setStatus("uploading")
      const res = await fetch(`${API}/uploads`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify({ filename: file.name}),
      })
      const { url, key } = await res.json()

      await fetch(url, {method: "PUT", body: file })
      setStatus("processing")
      const result = await pollForInvoice(key)
      setInvoice(result)
      setStatus("done")
    }
    catch{
      setStatus("error")
    }
  }

  return (
    <>
      <h1>Invoice Tax Calculator </h1>
      <input type="file" onChange={e=> setFile(e.target.files?.[0] ?? null)}/>
      <button onClick={handleUpload} disabled={!file}>Upload</button>
      <p>{status}</p>
      {invoice && (
        <div>
          <h2>{invoice.vendor}</h2>
          <p>Status: {invoice.status}</p>
          <table>
            <thead>
              <tr>
                <th>Description</th>
                <th>Category</th>
                <th>Amount</th>
                <th>Tax Rate</th>
                <th>Tax</th>
              </tr>
            </thead>
            <tbody>
              {invoice.line_items.map((item, i) => (
                <tr key={i}>
                  <td>{item.description}</td>
                  <td>{item.category}</td>
                  <td>{item.amount}</td>
                  <td>{item.tax_rate}</td>
                  <td>{item.tax_amount}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <p>Total tax: {invoice.total_tax}</p>
          {invoice.override_reason && <p>Override: {invoice.override_reason}</p>}
        </div>
      )}
    </>
  )
}
export default App
