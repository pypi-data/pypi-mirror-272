

def plot_topic_taxonomy_tree(clusters_list, file_name):

    def plot_cluster_tree(root, level, last=True, header='', writer=None):
        elbow = "└────"
        pipe = "│  "
        tee = "├────"
        blank = "   "
        print(f"{header}{elbow if last else tee} {root.topic} - {root.description} ({root.size} | {root.percentage*100:.1f}%)")
        if writer:
            writer.write(f"{header}{elbow if last else tee} {root.topic} - {root.description} ({root.size} | {root.percentage*100:.1f}%)\n")
        
        child_size = len(root.children_id)
        if child_size > 0:
            for i, c in enumerate(root.children_id):
                for cluster in clusters_list[level+1]:
                    if cluster.id == c:
                        plot_cluster_tree(cluster, level+1, header=header + (blank if last else pipe), last=i == child_size - 1, writer=writer)

    wf = open(file_name, "w")
    plot_cluster_tree(clusters_list[0][0], level=0, writer=wf)
    wf.close()