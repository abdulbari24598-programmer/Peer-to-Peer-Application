P2P File Transfer

This project is a simple implementation of a peer-to-peer (P2P) file transfer protocol, where peers can directly exchange files without relying on a central file server.

📌 Components

Manager

Tracks all active peers in the network.

Broadcasts updates when peers join or leave.

Peer

Connects to the manager to get the list of active peers.

Shares its files with others.

Requests and downloads files from other peers.

⚙️ How It Works

A new peer joins by pinging the manager, which responds with the list of all active peers.

When a peer needs a file, it queries the network to check which peers have it.

If multiple peers have the file, it downloads chunks from each of them in parallel.

Once all chunks are received, the file is reassembled and saved locally.

🚀 Running the Project

Start the manager:

python server.py

Start a peer:

python peer.py

On startup, you’ll be prompted to enter:

Port number

Peer name → must match the folder name inside the Peers/ directory.

📝 Usage

The manager continuously maintains a list of active peers.

This list is also written to logs/<peer_name>.log for reference.

From a peer, select option 3 (get_files) to request a file.

If found, the file is downloaded from other peers and stored in:

./Peers/<peer_name>/

💡 Example

Inside Peers/, there’s a folder a containing example.txt.

Run one peer with the name a.

Run another peer with the name b.

From peer b, request the file:

example.txt


The file will be transferred from peer a and saved in b’s folder.
