   
# Fonction pour cracker le mot de passe
def crack_password():
    global current_frame, current_progress, dernier_bouton_clique,c1
    hashed_password = entry_hashed_password.get().strip()
    
    if dernier_bouton_clique==1:
        if message_box_md5(hashed_password)==True:
            return
    elif dernier_bouton_clique==2:
        if message_box_sha1(hashed_password)==True:
            return
    else:
        if message_box_sha256(hashed_password)==True:
            return
    
    hide_all_frames()
    # Cacher tous les widgets sauf la barre de progression et le label clignotant
    label_hashed_password.place_forget()
    entry_hashed_password.place_forget()
    crack_button.place_forget()
    result_frame.place_forget()

    with open("liste.txt", "r") as file:
        words = [line.strip() for line in file]

    progress_bar.config(maximum=100)
    progress_bar.place(relx=0.5, rely=0.35, anchor='center')  # Centrer en hauteur et ajuster légèrement vers le haut
    percentage_label.place(relx=0.5, rely=0.28, anchor='center')  # Centrer en hauteur et ajuster légèrement vers le haut
    blink_label.place(relx=0.5, rely=0.45, anchor='center')  # Centrer en hauteur et ajuster légèrement vers le bas
    blink_dots(blink_label)  # Démarrer le clignotement des points
    current_frame = progress_bar
    c1.destroy()
    toggle_back_button(True)


    for progress in tqdm(range(101), desc="Chercher...", unit="%", leave=False):
        current_progress = progress
        progress_bar.config(value=current_progress)
        percentage_label.config(text=f"{current_progress}%")
        root.update()
        time.sleep(0.05)

    reset_progress_bar()  # Réinitialiser la barre de progression après la boucle

    progress_bar.place_forget()  # Cacher la barre de progression
    percentage_label.place_forget()  # Cacher le label de pourcentage
    blink_label.place_forget()  # Cacher le label clignotant

    if current_frame == progress_bar:
        if dernier_bouton_clique == 1:
            for word in words:
                md5_hash = hashlib.md5(word.encode()).hexdigest()
                if hashed_password == md5_hash:
                    result_label.config(text=f"Le mot de passe est :", fg=FG_COLOR)

                    return
        elif dernier_bouton_clique==2:
            for word in words:
                sha1_hash = hashlib.sha1(word.encode()).hexdigest()
                if hashed_password == sha1_hash:
                    result_label.config(text=f"Le mot de passe est :", fg=FG_COLOR)
                 
                    return
        else:
            for word in words:
                sha256_hash = hashlib.sha256(word.encode()).hexdigest()
                if hashed_password == sha256_hash:
                    result_label.config(text=f"Le mot de passe est :", fg=FG_COLOR)
                    
                    return


