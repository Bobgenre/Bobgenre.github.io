import React, { useState } from 'react';
import { Search, Info, Shield, Zap, Crosshair, Skull, Heart, Sword, Menu, Grid, List, ChevronRight, Filter } from 'lucide-react';

// Données des personnages (Roster complet à jour)
const characters = [
  { id: 1, name: "Sol Badguy", type: "Balance", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive.jpg", desc: "Le protagoniste. Frappe fort, facile à prendre en main." },
  { id: 2, name: "Ky Kiske", type: "Balance", difficulty: 1, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_kyk.jpg", desc: "L'all-rounder par excellence. Excellente portée et projectiles." },
  { id: 3, name: "May", type: "Rushdown", difficulty: 1, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_may-1.jpg", desc: "Dégâts explosifs avec ses dauphins. Simple et effrayante." },
  { id: 4, name: "Axl Low", type: "Zoning", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_axl.jpg", desc: "Le maître du combat à distance. Gardez l'ennemi loin." },
  { id: 5, name: "Chipp Zanuff", type: "Speed", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_chp.jpg", desc: "Le ninja ultra rapide. Très fragile mais invisible." },
  { id: 6, name: "Potemkin", type: "Grappler", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_pot.jpg", desc: "Un colosse lent. S'il vous attrape, c'est fini." },
  { id: 7, name: "Faust", type: "Unique", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_fau.jpg", desc: "Imprévisible grâce à ses objets aléatoires." },
  { id: 8, name: "Millia Rage", type: "Speed", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_mll.jpg", desc: "Reine du mix-up aérien. Laisse l'adversaire deviner." },
  { id: 9, name: "Zato-1", type: "Technical", difficulty: 5, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_zat.jpg", desc: "Contrôle deux entités à la fois (lui et l'ombre Eddie)." },
  { id: 10, name: "Ramlethal", type: "Shooting", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_ram-1.jpg", desc: "Domine le coin avec ses épées géantes." },
  { id: 11, name: "Leo Whitefang", type: "Balance", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_leo.jpg", desc: "Un gorille en armure. Excelle au corps à corps." },
  { id: 12, name: "Nagoriyuki", type: "One Shot", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_nag.jpg", desc: "Vampire samouraï. Gestion de la jauge de sang cruciale." },
  { id: 13, name: "Giovanna", type: "Rushdown", difficulty: 1, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2020/09/archive_gio.jpg", desc: "Facile, rapide et offensive. Idéale pour débuter." },
  { id: 14, name: "Anji Mito", type: "Balance", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2021/03/anji-306x305.jpg", desc: "Utilise des danses pour parer et contre-attaquer." },
  { id: 15, name: "I-No", type: "Rushdown", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2021/03/rxx82us-1-306x305.jpg", desc: "Mix-up constant grâce à son dash aérien unique." },
  { id: 16, name: "Goldlewis", type: "Power", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2021/07/gol-306x305.jpg", desc: "Dégâts massifs avec son cercueil. Behemoth Typhoon !" },
  { id: 17, name: "Jack-O'", type: "Technical", difficulty: 5, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2021/08/jko.jpg", desc: "Invoque des serviteurs pour contrôler le terrain." },
  { id: 18, name: "Happy Chaos", type: "Shooting", difficulty: 5, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2021/11/82nCeh3s.jpg", desc: "Utilise un pistolet pour zoner n'importe où." },
  { id: 19, name: "Baiken", type: "Balance", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2022/01/94gvos0f.jpg", desc: "Samouraï défensive avec des contres puissants." },
  { id: 20, name: "Testament", type: "Zoning", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2022/03/icon-1ubduiak.jpg", desc: "Contrôle l'espace avec magie et faux." },
  { id: 21, name: "Bridget", type: "Balance", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2022/08/38nd9nd2jd73.jpg", desc: "Longue portée et mobilité avec ses yoyos." },
  { id: 22, name: "Sin Kiske", type: "Rushdown", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2022/11/n5idg73diw3.jpg", desc: "Combos étendus, mais doit manger pour recharger." },
  { id: 23, name: "Bedman?", type: "Unique", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2023/03/5fve3hdwci.jpg", desc: "Lit qui se bat tout seul. Gameplay erratique." },
  { id: 24, name: "Asuka R#", type: "Technical", difficulty: 5, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2023/05/xnNj771Auw.jpg", desc: "Le roi de la magie. Gameplay basé sur des cartes RNG." },
  { id: 25, name: "Johnny", type: "Zoning", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2023/08/archive_4ny9b-6nvi.jpg", desc: "Maître du Iaido. Élégant et létal à mi-distance." },
  { id: 26, name: "Elphelt", type: "Rushdown", difficulty: 1, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2023/12/4nf89dcoo3.jpg", desc: "Guns & Roses. Gameplay offensif très direct." },
  { id: 27, name: "A.B.A", type: "Unique", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2024/03/3uf9vnso76.jpg", desc: "Doit activer son mode Rage pour être efficace." },
  { id: 28, name: "Slayer", type: "Power", difficulty: 2, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2024/04/4tg8hdo2.jpg", desc: "Dandy vampire. Frappes lourdes et imprévisibles." },
  { id: 29, name: "Queen Dizzy", type: "Zoning", difficulty: 4, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2018/10/archive-ny040fsi2.jpg", desc: "Reine de Illyria. Contrôle le terrain avec Necro et Undine." },
  { id: 30, name: "Venom", type: "Technical", difficulty: 5, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2025/03/adhfjha.jpg", desc: "L'assassin boulanger. Maître du billard magique." },
  { id: 31, name: "Lucy", type: "Speed", difficulty: 3, image: "https://guiltygear.com/ggst/en/common/img/character/lucy/stand.png", desc: "Invité de Cyberpunk. Hackeuse agile armée de monowires." },
  { id: 32, name: "Unika", type: "Unique", difficulty: 3, image: "https://www.guiltygear.com/ggst/en/wordpress/wp-content/uploads/2025/05/khfauiy.jpg", desc: "Protagoniste de l'anime Dual Rulers. Une mystérieuse chasseuse de Gears." },
];

const DifficultyPill = ({ level }) => {
  let color = "bg-green-500/20 text-green-400";
  let text = "Facile";
  
  if (level === 3) {
     color = "bg-yellow-500/20 text-yellow-400";
     text = "Moyen";
  } else if (level >= 4) {
     color = "bg-red-500/20 text-red-400";
     text = "Difficile";
  }

  return (
    <span className={`text-xs px-2 py-1 rounded font-medium ${color}`}>
      {text}
    </span>
  );
};

export default function App() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedType, setSelectedType] = useState("Tous");

  const types = ["Tous", "Balance", "Rushdown", "Zoning", "Power", "Speed", "Grappler", "Technical", "Unique", "Shooting", "One Shot"];

  const filteredCharacters = characters.filter(char => {
    const matchesSearch = char.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedType === "Tous" || char.type === selectedType;
    return matchesSearch && matchesType;
  });

  return (
    <div className="flex h-screen bg-[#0B1120] text-slate-200 font-sans overflow-hidden">
      
      {/* Sidebar - Style inspiré de la capture (Paquets/Menu à gauche) */}
      <aside className="w-64 bg-[#111827] flex-shrink-0 flex flex-col border-r border-slate-800">
        <div className="p-6">
          <h1 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
            <span className="w-8 h-8 bg-orange-600 rounded flex items-center justify-center text-white font-black">GG</span>
            Strive
          </h1>
          
          <div className="space-y-6">
            <div>
              <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Menu</h2>
              <button 
                onClick={() => setSelectedType("Tous")}
                className={`w-full text-left px-4 py-3 rounded-lg font-medium transition-all duration-200 flex items-center justify-between group ${selectedType === "Tous" ? 'bg-orange-600 text-white shadow-lg shadow-orange-900/20' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
              >
                <span>Tous les persos</span>
                {selectedType === "Tous" && <ChevronRight size={16} />}
              </button>
            </div>

            <div>
              <div className="flex items-center justify-between mb-3 px-1">
                 <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Archétypes</h2>
                 <span className="text-[10px] bg-slate-800 px-1.5 py-0.5 rounded text-slate-500">{types.length - 1}</span>
              </div>
              
              <div className="space-y-1">
                {types.filter(t => t !== "Tous").map(type => (
                  <button
                    key={type}
                    onClick={() => setSelectedType(type)}
                    className={`w-full text-left px-4 py-2.5 rounded-md text-sm transition-colors flex items-center justify-between
                      ${selectedType === type 
                        ? 'bg-orange-600/10 text-orange-500 border border-orange-600/20' 
                        : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800'
                      }`}
                  >
                    <span>{type}</span>
                    {selectedType === type && <div className="w-1.5 h-1.5 rounded-full bg-orange-500"></div>}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>

        <div className="mt-auto p-4 border-t border-slate-800">
           <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-slate-700 flex items-center justify-center text-xs font-bold">U</div>
              <div className="text-sm">
                 <p className="text-white font-medium">Utilisateur</p>
                 <p className="text-slate-500 text-xs">Invité</p>
              </div>
           </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 bg-[#0f141f]">
        
        {/* Top Bar styled as search area */}
        <div className="h-16 border-b border-slate-800 flex items-center px-8 justify-between bg-[#0f141f]/50 backdrop-blur-sm sticky top-0 z-20">
           <h2 className="text-lg font-semibold text-orange-500 flex items-center gap-2">
             {selectedType === "Tous" ? "Roster Complet" : `Classe : ${selectedType}`}
             <span className="bg-slate-800 text-slate-400 text-xs px-2 py-0.5 rounded-full font-normal">
               {filteredCharacters.length}
             </span>
           </h2>

           <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
              <input 
                type="text" 
                placeholder="Rechercher..." 
                className="bg-slate-900 border border-slate-700 text-slate-200 pl-10 pr-4 py-1.5 rounded-md text-sm focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 w-64 transition-all"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
           </div>
        </div>

        {/* Content Scrollable */}
        <div className="flex-1 overflow-y-auto p-8">
           
           {/* Stats Cards Row (Inspiré des compteurs verts/oranges) */}
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 flex items-center justify-between">
                 <div>
                    <p className="text-slate-400 text-sm">Personnages Total</p>
                    <p className="text-2xl font-bold text-white">{characters.length}</p>
                 </div>
                 <div className="p-3 bg-slate-700/50 rounded-lg text-slate-400">
                    <Grid size={20} />
                 </div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 flex items-center justify-between">
                 <div>
                    <p className="text-slate-400 text-sm">Débutant (Facile)</p>
                    <p className="text-2xl font-bold text-green-400">
                       {characters.filter(c => c.difficulty <= 2).length}
                    </p>
                 </div>
                 <div className="p-3 bg-green-900/20 rounded-lg text-green-500">
                    <Heart size={20} />
                 </div>
              </div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-lg p-4 flex items-center justify-between">
                 <div>
                    <p className="text-slate-400 text-sm">Technique (Difficile)</p>
                    <p className="text-2xl font-bold text-orange-400">
                       {characters.filter(c => c.difficulty >= 4).length}
                    </p>
                 </div>
                 <div className="p-3 bg-orange-900/20 rounded-lg text-orange-500">
                    <Skull size={20} />
                 </div>
              </div>
           </div>

           {/* Characters Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
             {filteredCharacters.map((char) => (
               <div 
                 key={char.id}
                 className="bg-[#1e293b] rounded-xl overflow-hidden border border-slate-700 hover:border-orange-500/50 hover:shadow-lg hover:shadow-orange-900/10 transition-all duration-300 group flex flex-col"
               >
                 {/* Image Container - Clean cut */}
                 <div className="relative h-48 bg-slate-800 overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-t from-[#1e293b] to-transparent opacity-80 z-10" />
                    <img 
                      src={char.image} 
                      alt={char.name}
                      className="w-full h-full object-cover object-top transform group-hover:scale-105 transition-transform duration-500"
                      onError={(e) => {
                         e.target.src = `https://placehold.co/400x600/1e293b/cbd5e1?text=${char.name}`;
                      }}
                    />
                    <div className="absolute top-3 right-3 z-20">
                       <DifficultyPill level={char.difficulty} />
                    </div>
                 </div>

                 <div className="p-5 flex-1 flex flex-col">
                    <div className="flex justify-between items-start mb-2">
                       <h3 className="text-lg font-bold text-white group-hover:text-orange-400 transition-colors">{char.name}</h3>
                    </div>
                    
                    <p className="text-slate-400 text-sm leading-relaxed mb-4 line-clamp-2 flex-1">
                       {char.desc}
                    </p>

                    <div className="pt-4 border-t border-slate-700 flex items-center justify-between">
                       <span className="text-xs font-medium text-slate-500 uppercase tracking-wider bg-slate-900 px-2 py-1 rounded">
                          {char.type}
                       </span>
                       <button className="text-orange-500 hover:text-orange-400 transition-colors p-1 rounded hover:bg-orange-500/10">
                          <Info size={18} />
                       </button>
                    </div>
                 </div>
               </div>
             ))}
           </div>
           
           {filteredCharacters.length === 0 && (
             <div className="h-64 flex flex-col items-center justify-center text-slate-500 bg-slate-800/30 rounded-xl border border-dashed border-slate-700">
               <Filter size={48} className="mb-4 opacity-50" />
               <p className="text-lg font-medium">Aucun combattant trouvé</p>
               <button 
                 onClick={() => {setSearchTerm(""); setSelectedType("Tous");}}
                 className="mt-2 text-orange-500 hover:underline text-sm"
               >
                 Réinitialiser les filtres
               </button>
             </div>
           )}

        </div>
      </main>
    </div>
  );
}