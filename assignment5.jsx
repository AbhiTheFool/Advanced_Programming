import { useState } from "react";

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");

  function addTodo() {
    if (text !== "") {
      setTodos([...todos, text]);
      setText("");
    }
  }

  return (
    <div>
      <h2>Todo List</h2>

      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default TodoApp;
