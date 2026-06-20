using System;
using System.Collections.Generic;

namespace ModernNetworkSimulation
{
    // 1. INTERFACES
    public interface IDevice
    {
        string Name { get; set; }
        bool SwitchedOn { get; set; }
        void StartDevice();
        void ShutDown();
    }

    public interface INetworkable : IDevice
    {
        string Ipaddress { get; set; }
        void ReceivePing(string fromDevice, string message);
    }


    // 2. CENTRAL IP AND NETWORK REGISTRY
    public static class NetworkRegistry
    {
        private static int _currentHost = 10;
        private static readonly HashSet<string> AllocatedIps = new HashSet<string>();

        public static string RegisterIp(string requestedIp = null)
        {
            if (!string.IsNullOrEmpty(requestedIp))
            {
                if (AllocatedIps.Contains(requestedIp))
                    throw new InvalidOperationException($"[IP CONFLICT] The address {requestedIp} is already in use!");
                
                AllocatedIps.Add(requestedIp);
                return requestedIp;
            }

            string newIp;
            do
            {
                newIp = $"10.0.0.{++_currentHost}";
            } while (AllocatedIps.Contains(newIp));

            AllocatedIps.Add(newIp);
            return newIp;
        }
    }


    // 3. CLASSES
    public class Computer : INetworkable
    {
        public string Name { get; set; }
        public string Make { get; set; }
        public string OperatingSystem { get; set; }
        public bool SwitchedOn { get; set; }
        public string Ipaddress { get; set; }

        public Computer(string name, string make, string osystem, bool switched, string manualIp = null)
        {
            Name = name;
            Make = make;
            OperatingSystem = osystem;
            SwitchedOn = switched;
            Ipaddress = NetworkRegistry.RegisterIp(manualIp);
        }

        public virtual void StartDevice()
        {
            if (!SwitchedOn)
            {
                SwitchedOn = true;
                Console.WriteLine($"[SYSTEM] {Name} is loading {OperatingSystem} and starting up...");
            }
        }

        public virtual void ShutDown()
        {
            if (SwitchedOn)
            {
                SwitchedOn = false;
                Console.WriteLine($"[SYSTEM] {Name} has been shut down safely.");
            }
        }

        public virtual void ReceivePing(string fromDevice, string message)
        {
            Console.WriteLine($"[{Name} - Computer]: -> Received packet from {fromDevice}: '{message}'");
        }
    }

    public class Server : Computer
    {
        public string ServiceType { get; set; }

        public Server(string name, string make, string osystem, bool switched, string serviceType, string manualIp = null) 
            : base(name, make, osystem, switched, manualIp)
        {
            ServiceType = serviceType;
        }

        public override void ShutDown()
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.Write($"\n[CRITICAL WARNING] '{Name}' is a SERVER ({ServiceType}). Shut down? (YES/no): ");
            Console.ResetColor();
            
            string confirm = Console.ReadLine();
            if (confirm?.ToUpper() == "YES")
            {
                base.ShutDown();
            }
            else
            {
                Console.WriteLine($"[SYSTEM] Shutdown canceled. Server {Name} remains online.");
            }
        }

        public override void StartDevice()
        {
            if (!SwitchedOn)
            {
                base.StartDevice();
                Console.WriteLine($"[SERVICE] '{ServiceType}' services have been initialized on {Name}.");
            }
        }

        public override void ReceivePing(string fromDevice, string message)
        {
            Console.WriteLine($"[{Name} - Server]: -> Request handled by '{ServiceType}' service for client {fromDevice}.");
        }
    }

    public class NetworkPrinter : INetworkable
    {
        public string Name { get; set; }
        public string Ipaddress { get; set; }
        public bool SwitchedOn { get; set; }
        public string PrinterModel { get; set; }

        public NetworkPrinter(string name, string model, bool switched)
        {
            Name = name;
            PrinterModel = model;
            SwitchedOn = switched;
            Ipaddress = NetworkRegistry.RegisterIp();
        }

        public void StartDevice()
        {
            if (!SwitchedOn)
            {
                SwitchedOn = true;
                Console.WriteLine($"[PRINTER] {Name} ({PrinterModel}) online and ready.");
            }
        }

        public void ShutDown()
        {
            if (SwitchedOn)
            {
                SwitchedOn = false;
                Console.WriteLine($"[PRINTER] {Name} is entering power-saving sleep mode.");
            }
        }

        public void ReceivePing(string fromDevice, string message)
        {
            Console.WriteLine($"[{Name} - Printer]: -> Print queue acknowledged by {fromDevice}. Status: OK.");
        }
    }

    public class Router
    {
        public string RouterName { get; set; }
        private readonly List<INetworkable> _connectedDevices = new List<INetworkable>();

        public Router(string name)
        {
            RouterName = name;
        }

        public void ConnectDevice(INetworkable device)
        {
            _connectedDevices.Add(device);
        }

        public List<INetworkable> GetDevices() => _connectedDevices;

        public void RoutePing(string fromIp, string toIp, string message = "Ping Packet")
        {
            INetworkable sender = _connectedDevices.Find(d => d.Ipaddress == fromIp);
            INetworkable receiver = _connectedDevices.Find(d => d.Ipaddress == toIp);

            Console.WriteLine($"\n[ROUTER - {RouterName}] -> Routing data packet...");

            if (sender == null)
            {
                Console.WriteLine("[ERROR] Source device not found in this routing table!");
                return;
            }
            if (!sender.SwitchedOn)
            {
                Console.WriteLine($"[ERROR] {sender.Name} cannot send data. It is powered OFF!");
                return;
            }
            if (receiver == null)
            {
                Console.WriteLine($"[ERROR] Destination IP {toIp} is unreachable (404 Not Found).");
                return;
            }
            if (!receiver.SwitchedOn)
            {
                Console.WriteLine($"[ERROR] Destination {receiver.Name} ({receiver.Ipaddress}) is Down/Offline.");
                return;
            }

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine($"[LINK ACTIVE] {sender.Name} ({sender.Ipaddress}) ===> {receiver.Name} ({receiver.Ipaddress})");
            Console.ResetColor();

            var rnd = new Random();
            for (int i = 1; i <= 3; i++)
            {
                double ms = Math.Round(rnd.NextDouble() * 4 + 1, 2);
                Console.WriteLine($"   64 bytes from {receiver.Ipaddress}: icmp_seq={i} ttl=64 time={ms} ms");
            }
            
            deviceReceivedLog(receiver, sender.Name, message);
        }

        private void deviceReceivedLog(INetworkable receiver, string senderName, string message)
        {
            receiver.ReceivePing(senderName, message);
        }

        public void ShowNetworkReport()
        {
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("\n╔═════════════════════════════════════════════════════════════════════════════╗");
            Console.WriteLine("║                 Active Network Infrastructure Report                        ║");
            Console.WriteLine("╚═════════════════════════════════════════════════════════════════════════════╝");
            Console.ResetColor();

            Console.BackgroundColor = ConsoleColor.DarkGray;
            Console.ForegroundColor = ConsoleColor.White;
            Console.WriteLine(
                " │ " + "Device Name".PadRight(14) + 
                " │ " + "IP Address".PadRight(14) + 
                " │ " + "Status".PadRight(16) + 
                " │ " + "Type / Extra Info".PadRight(23) + " │"
            );
            Console.ResetColor();
            Console.WriteLine(" ├────────────────┼────────────────┼──────────────────┼─────────────────────────┤");

            foreach (var device in _connectedDevices)
            {
                string name = device.Name.PadRight(14);
                string ip = device.Ipaddress.PadRight(14);
                
                string typeInfo = device.GetType().Name;
                if (device is Server s)
                    typeInfo += $" [{s.ServiceType}]";
                else if (device is NetworkPrinter p)
                    typeInfo += $" [{p.PrinterModel}]";
                
                typeInfo = typeInfo.PadRight(23);

                string statusText = device.SwitchedOn ? "● ONLINE (Up)" : "○ OFFLINE (Down)";
                statusText = statusText.PadRight(16);

                Console.Write(" │ " + name + " │ " + ip + " │ ");

                if (device.SwitchedOn) Console.ForegroundColor = ConsoleColor.Green;
                else Console.ForegroundColor = ConsoleColor.Red;
                
                Console.Write(statusText);
                Console.ResetColor();
                Console.WriteLine(" │ " + typeInfo + " │");
            }

            Console.WriteLine(" └────────────────┴────────────────┴──────────────────┴─────────────────────────┘\n");
        }
    }


    // 4. MAIN PROGRAM
    class Program
    {
        static void Main(string[] args)
        {
            Router centralRouter = new Router("Cisco-881");

            Server dhcpServer = new Server("DHCP-SRV", "Dell", "Linux", true, "IP Allocation", "10.0.0.1");
            Server webServer = new Server("Web-SRV", "IBM", "Linux", true, "Nginx Web", "10.0.0.2");
            Computer pcAlfa = new Computer("PC-Alfa", "HP", "Windows 11", true);
            Computer pcBeta = new Computer("PC-Beta", "Lenovo", "Ubuntu", false);
            NetworkPrinter laserPrinter = new NetworkPrinter("Printer-Main", "HP LaserJet", true);

            centralRouter.ConnectDevice(dhcpServer);
            centralRouter.ConnectDevice(webServer);
            centralRouter.ConnectDevice(pcAlfa);
            centralRouter.ConnectDevice(pcBeta);
            centralRouter.ConnectDevice(laserPrinter);

            bool running = true;
            
            // İlk açılış raporu
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("=== MODERN OOP NETWORK SIMULATION PANEL ===");
            Console.ResetColor();
            centralRouter.ShowNetworkReport();

            while (running)
            {
                Console.WriteLine("1. Power ON a Device");
                Console.WriteLine("2. Power OFF a Device");
                Console.WriteLine("3. Send Smart Ping (Through Router)");
                Console.WriteLine("4. Exit");
                Console.Write("\nYour Choice (1-4): ");

                string choice = Console.ReadLine();
                var devices = centralRouter.GetDevices();

                switch (choice)
                {
                    case "1":
                        Console.Write("\nEnter device name to Power ON: ");
                        string openName = Console.ReadLine();
                        var devToOpen = devices.Find(d => d.Name.Equals(openName, StringComparison.OrdinalIgnoreCase));
                        if (devToOpen != null) devToOpen.StartDevice();
                        else Console.WriteLine("Device not found!");
                        ShowUpdate(centralRouter);
                        break;

                    case "2":
                        Console.Write("\nEnter device name to Power OFF: ");
                        string closeName = Console.ReadLine();
                        var devToClose = devices.Find(d => d.Name.Equals(closeName, StringComparison.OrdinalIgnoreCase));
                        if (devToClose != null) devToClose.ShutDown();
                        else Console.WriteLine("Device not found!");
                        ShowUpdate(centralRouter);
                        break;

                    case "3":
                        Console.WriteLine("\n--- PING CONTROL PANEL ---");
                        Console.Write("Source device name (e.g., PC-Alfa): ");
                        string fromName = Console.ReadLine();
                        var senderDev = devices.Find(d => d.Name.Equals(fromName, StringComparison.OrdinalIgnoreCase));

                        Console.Write("Destination IP address (e.g., 10.0.0.2): ");
                        string targetIp = Console.ReadLine();

                        if (senderDev != null)
                        {
                            centralRouter.RoutePing(senderDev.Ipaddress, targetIp, "Infrastructure check payload.");
                        }
                        else
                        {
                            Console.WriteLine("Source device not found!");
                        }
                        ShowUpdate(centralRouter);
                        break;

                    case "4":
                        running = false;
                        Console.WriteLine("\nSimulation stopped. Good bye!");
                        break;

                    default:
                        Console.WriteLine("\nInvalid choice! Pick a number between 1 and 4.\n");
                        break;
                }
            }
        }

        static void ShowUpdate(Router router)
        {
            Console.WriteLine("\n-------------------------------------------------------------------------");
            Console.ForegroundColor = ConsoleColor.DarkYellow;
            Console.WriteLine("[NETWORK UPDATE] Present Infrastructure Status:");
            Console.ResetColor();
            router.ShowNetworkReport();
        }
    }
}