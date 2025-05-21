import React from 'react'

export default function ActionModal({ show, onClose, onAction }) {
  if (!show) return null
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white p-4 rounded">
        <h3 className="font-bold mb-2">Choisissez une action</h3>
        <button onClick={() => onAction({ type: 'income' })}>Revenu</button>
        <button onClick={() => onAction({ type: 'foreign_aid' })}>Aide étrangère</button>
        <button onClick={() => onAction({ type: 'coup' })}>Coup (7 pièces)</button>
        <button onClick={onClose}>Annuler</button>
      </div>
    </div>
  )
}