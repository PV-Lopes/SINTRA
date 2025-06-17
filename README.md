# 🚦SINTRA (Sistema Inteligente de Prevenção de Sinistros no Trânsito)

## 🧭 Overview

**SIPAT** Sistema Inteligente de Prevençao de Acidentes de Trânsito...

---
## Website link:

https://webapp-sabor-caseiro.azurewebsites.net (remover ou substituir)

## ✅ Features

- Table reservation with date and time (remover ou substituir)
- Order management (remover ou substituir)
- Scalable backend using Node.js
- Automatic CI/CD through GitHub Actions
- Infrastructure as Code (IaC) using Terraform
- Azure-ready deployment

---

## 🛠️ Tech Stack

- **Node.js** 
- **Express**
- **Terraform (Azure Provider)**
- **GitHub Actions**
- **VSCode + JSON Configs**

---

## 📁 Project Structure
```bash
├── .github                     # GitHub Actions for CI/CD
│   └── workflows               # Contains workflow definitions
│       └── deploy.yml          # Workflow file that automates the deployment process
├── public                      # Static assets served by the web application
│   ├── css                     # Stylesheets (CSS)
│   ├── img                     # Image assets
│   ├── script                  # Front-end JavaScript files
│   └── index.html              # Main HTML file for the web interface
├── app.js                      # Express server
├── package.json                # Dependencies
├── Staging/                    # Infrastructure using Terraform
│   ├── main.tf                 # Azure infrastructure definition
│   └── terraform.tfstate       # Terraform state file
├── README.md                   # Project documentation
```

---

## 📦 Installation Guide

### Prerequisites

| Technology | Recommended Version |
|------------|---------------------|
| Node.js    | >= 18.x             |
| NPM        | >= 9.x              |
| Terraform  | >= 1.5              |
| Azure Account | ✔️ Required       |

---

### Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-user/Sabor-Caseiro-Restaurant.git
cd Sabor-Caseiro-Restaurant

# 2. Install dependencies
npm install

# 3. Run the application
node app.js
```

> The app will be available at:
```
http://localhost:3000
```

---

### Cloud Deployment with Terraform (Azure)

1. Authenticate via Azure CLI  
```bash
az login
```

2. Go to the `Staging/` folder  
```bash
cd Staging/
```

3. Initialize Terraform  
```bash
terraform init
```

4. Apply the provisioning plan  
```bash
terraform apply
```
5. Confirm with `yes` when prompted

---

## 🔌 API Reference

### `GET /`

- **Description:** Returns the system’s welcome message.
- **Response:**
```json
{
  "message": "Welcome to Sabor Caseiro Restaurant!"
}
```

---

### `POST /reserva`

- **Description:** Create a new table reservation.
- **Request Body:**
```json
{
  "nome": "John",
  "mesa": 5,
  "data": "2025-06-10",
  "hora": "19:30"
}
```

- **Response:**
```json
{
  "status": "Reservation confirmed",
  "reservaId": "abc123"
}
```

---

### `GET /pedidos`

- **Description:** Fetch all active orders.
- **Response:**
```json
[
  {
    "pedidoId": "xyz789",
    "mesa": 5,
    "itens": ["Lasagna", "Orange Juice"]
  }
]
```

---

## 🤝 Contribution Guide

### How to Contribute

1. **Fork the repository**  
2. **Create a feature branch:**  
```bash
git checkout -b feature/your-feature
```
3. **Commit your changes with meaningful messages:**  
```bash
git commit -m "feat: add new orders endpoint"
```
4. **Push your branch and open a Pull Request**

---

### Pull Request Rules

- Follow the existing code style in `app.js`
- Always document new endpoints in the API section
- Include basic testing where applicable

---

## 📞 Contact
- 👤 Developer: Rayra Lima
- 📧 Email: rayrasilvafiction@gmail.com  
- 🌐 GitHub: https://github.com/Rayralima

---

## 🛡️ License

Este é um projeto para fins educacionais 


˙✧˖°🦊 ༘ ⋆｡˚
