import { ByteBuffer } from 'flatbuffers';
import { State } from '../generated/test-interface/state';

const localState = {
  pointer: [0, 0, 0],
  offset: null as number | null,
  hp: null as number | null,
  message: null as string | null,
  status: null as number | null,
  distance: null as number | null,
};

function log(msg: string) {
  const logEl = document.getElementById('log') as HTMLDivElement;
  const line = document.createElement('div');
  line.textContent = msg;
  logEl.prepend(line);
  while (logEl.children.length > 50) logEl.removeChild(logEl.lastChild!);
}

function updateFromFlatBuffer(bytes: ArrayBuffer) {
  const buf = new ByteBuffer(new Uint8Array(bytes));
  const state = State.getRootAsState(buf);

  const vec = state.pointer();
  if (vec) {
    localState.pointer = [vec.x(), vec.y(), vec.z()];
  }
  localState.distance = state.distance();

  if (state.offset() !== null) localState.offset = state.offset();
  if (state.hp() !== null) localState.hp = state.hp();
  if (state.message() !== null) localState.message = state.message();
  if (state.status() !== null) localState.status = state.status();
}

function compare(json: any): boolean {
  return (
    localState.offset === json.offset &&
    localState.hp === json.hp &&
    localState.message === json.message &&
    localState.status === json.status &&
    localState.distance === json.distance
  );
}

export function startWebSocket() {
  let msgCount = 0;
  let goodCount = 0;
  let pendingBinary: ArrayBuffer | null = null;

  const ws = new WebSocket('ws://localhost:8000/ws/json');
  ws.binaryType = 'arraybuffer';

  ws.onmessage = (event) => {
    if (event.data instanceof ArrayBuffer) {
      pendingBinary = event.data;
    } else {
      if (!pendingBinary) return;

      updateFromFlatBuffer(pendingBinary);
      const json = JSON.parse(event.data);

      if (compare(json)) {
        goodCount++;
        log(`✓ #${msgCount + 1} offset:${localState.offset} hp:${localState.hp} msg:${localState.message} status:${localState.status} dist:${localState.distance}`);
      } else {
        log(`✗ #${msgCount + 1} MISMATCH`);
      }
      msgCount++;
      pendingBinary = null;

      document.getElementById('stats')!.textContent =
        `Mensajes: ${msgCount} | OK: ${goodCount}`;
    }
  };

  ws.onclose = () => {
    const success = msgCount > 0 && goodCount === msgCount;
    const el = document.getElementById('result')!;
    el.textContent = success ? '1' : '0';
    el.style.color = success ? 'green' : 'red';
  };
}