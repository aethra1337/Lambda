//The concepts of OOP in C#
//Abstract classes
//Older version

using System;
using System.Collections.Generic;

namespace OOP_in_Csharp
{

	//-------------------------------
	public abstract class Device
	{
		public  Device(string name, string make)
		{
			_name = name;
			_make = make;
		}

		protected string _name;
		protected string _make;
		public abstract void StartDevice();
		public abstract void ShutDown();

	}
	//--------------------------------

	public class Computer : Device
	{
		public Computer (string name, string make, string osystem, bool switched) : base(name, make)
		{
			//this.Name = name;
			//this.Make = make;
			this.OperatingSystem = osystem;
			this.SwitchedOn = switched;
			compCounter++;
		}

	

		// private member variables
		//protected string _name;
		protected string _ipadress;
		protected bool _switchedOn;
		//protected string _make;
		protected string _operatingSystem;

		protected static int compCounter = 0; //counts comps in the network
		protected static int switchedCounter = 0; //counts comps that are switched
		protected static int compInNet = 10; //the first comp in the network

		public static int CountComps ()
		{
			return compCounter;
		}

		public static int CountSwitched ()
		{
			return switchedCounter;
		}

		public override void StartDevice () 
		{   
			this.SwitchedOn = true; 
			switchedCounter++;
			this.Ipaddress = GetIpAddress();
			Console.WriteLine("The comp {0} is starting ...", this.Name);
		}

		public override void ShutDown() 
		{
			this.SwitchedOn = false; 
			switchedCounter--;
			Console.WriteLine("The comp {0} is shuting down !!!", this.Name);
		}

		public string IsSwitched() 
		{
			if (this.SwitchedOn) 
			{ return "switched ON"; }
			else
			{ return "switched OFF"; }
		}

		// public properties
		public string Name
		{
			get { return _name;  }
			set { _name = value; }
		}
		public string Ipaddress
		{
			get { return _ipadress;  }
			set { _ipadress = value; }
		}
		public string Make
		{ 
			get { return _make; }
			set { _make = value; }
		}
		public string OperatingSystem
		{ 
			get { return _operatingSystem; }
			set { _operatingSystem = value; }
		}
		public bool SwitchedOn
		{
			get { return _switchedOn; }
			set { _switchedOn = value; }
		}

		public static void ShowComputers (List<Computer> net)
		{
			foreach (Computer comp in net) 
			{
				if (comp.SwitchedOn) 
				{
					Type type = comp.GetType();
					string stringType = type.ToString ();
					Console.Write("{0}\t{1}\t{2}\t\t{3}", comp.Name, comp.Ipaddress, comp.OperatingSystem, comp.Make);
					int pos = stringType.IndexOf('.');
					//Console.Write(stringType.Substring(pos+1,4));

					if(stringType.Substring(pos+1,4) == "Serv")
					{
						Server serv = (Server) comp;
						System.Console.WriteLine("\t{0}", serv.Destination);
					}
					else
						Console.WriteLine();	
				}   

			}	    
		} // end of ShowComputers

		public static void PingToComputer (List<Computer> net, Computer pingFrom, string pingTo)
		{
			Random rnd = new Random();
			double answer;
			Computer myComp = pingFrom;
			bool found = false;	
			Console.WriteLine("\nTrying to ping from the machine{0}({1}) to {2}.", myComp.Name, myComp.Ipaddress, pingTo);
			Console.WriteLine("--------------------------------------------------------------------");
			foreach (Computer comp in net) 			 	
			{
				if ((pingTo == comp.Ipaddress) && (comp.SwitchedOn == true)) 
				{
					found = true;
					break;
				} 
			} // the end of the loop
			if (found) 
			{ 
				for (int i = 5; i < 15; i++) 
				{ 
					answer = (float)(rnd.Next(1, 100))/100;
					Console.WriteLine ("64 bytes from {0} icmp_seq={1} ttl=64 time={2} ms", myComp.Ipaddress, i.ToString(), answer.ToString());
				}
			}	
			else
			{					
				Console.WriteLine ("Adress {0} not found !!! ", pingTo );
			} 
		} //end of PingToComputer method

		public string GetIpAddress()
		{
			string address = "10.0.0." + (++compInNet).ToString();
			return address;
		}
	} //end of the class Computer



	//--------------------------------
	public class Server : Computer
	{
		public Server (string name, string make, string osystem, bool switched, string dest, string ip) : base(name, make, osystem, switched)
		{			
			this.Destination = dest;
			this.Ipaddress = ip;
		}

		// private member variables
		private string _destination;

		// public properties
		public string Destination
		{
			get { return _destination;  }
			set { _destination = value; }
		}

		public override void ShutDown() 
		{   
			Console.WriteLine("************* !!! **************** ");
			Console.Write("You want to shut dowm this server. Are you sure ? (YES/n): ");


			string confirm = Console.ReadLine();
			if (confirm == "YES") 
			{
    			this.SwitchedOn = false; 
    			switchedCounter--;
    			Console.WriteLine("The comp {0} is shuting down !!!", this.Name);
			}

		}

		public override void StartDevice() 
		{   
			this.SwitchedOn = true; 
			switchedCounter++;
			Console.WriteLine("The comp {0} is starting ...", this.Name);
		}
	} //end of the class Server

	//--------------------------------
	class Program
	{
		public static void Main (string[]args)
		{
			List<Computer> network = new List<Computer>();          

			//Creating the objects 
			Server   zero = new Server ("zero",  "Dell", "Linux", false, "DHCP", "10.0.0.1");
			Server   omega = new Server ("omega", "IBM", "Linux", false, "WEB Server", "10.0.0.2");
			Server   mysql = new Server ("mysql", "IBM", "Linux", false, "MySql", "10.0.0.5");
			Computer alfa = new Computer ("alfa", "Dell", "Windows", false);
			Computer beta = new Computer ("beta", "Lenovo", "Linux", false);
			Computer gamma = new Computer ("gamma", "HP", "Windows", false);
			Computer delta = new Computer ("delta", "Dell", "Windows", false);

			//Adding objects Computer to the list network
			network.Add(zero);
			network.Add(omega);
			network.Add(mysql);
			network.Add(alfa);              
			network.Add(beta);
			network.Add(gamma);
			network.Add(delta);

			int compsInNetwork = Computer.CountComps ();
			Console.WriteLine ("We have {0} computers in our network.\n", compsInNetwork);

			//"Swithing on the computers"
			for(int i=0; i<network.Count; i++) 
			{
				network[i].StartDevice();       
			}

			Console.WriteLine ("We have {0} computers in our network that is switched ON\n", Computer.CountSwitched());	   
			Computer.ShowComputers(network);    
			Console.WriteLine ("\n--------------------------------------------------------------------"); 
			//omega.ShutDown();
			beta.ShutDown();
			Console.WriteLine ("--------------------------------------------------------------------"); 
			Console.WriteLine ("\nWe have {0} computers in our network that is switched ON\n", Computer.CountSwitched());	   
			Computer.ShowComputers(network);    

			//Ping from alfa to 10.0.0.14
			Computer.PingToComputer(network, alfa, "10.0.0.14");
		}
	}
}

