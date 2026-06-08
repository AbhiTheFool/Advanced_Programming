import java.util.*;
import java.util.stream.Collectors;
import java.util.AbstractMap.SimpleEntry;

class Pupil {
    private final int rollNo;
    private final String fullName;
    private final List<String> subjects;
    private final Map<String, Integer> grades;

    public Pupil(int rollNo, String fullName, List<String> subjects, Map<String, Integer> grades) {
        this.rollNo = rollNo;
        this.fullName = fullName;
        this.subjects = List.copyOf(subjects);
        this.grades = Map.copyOf(grades);
    }

    public int getRollNo() { return rollNo; }
    public String getFullName() { return fullName; }
    public List<String> getSubjects() { return subjects; }

    public int fetchGrade(String subject) {
        return grades.getOrDefault(subject, 0);
    }

    public double calculateMean() {
        return subjects.stream()
                .mapToInt(this::fetchGrade)
                .average()
                .orElse(0.0);
    }
}

public class StudentAnalyzer {

    public static List<Pupil> findLeadingPerformers(List<Pupil> group, int limit) {
        if (group == null || group.isEmpty() || limit <= 0) {
            return Collections.emptyList();
        }

        return group.stream()
                .sorted(Comparator.comparingDouble(Pupil::calculateMean).reversed())
                .limit(limit)
                .toList();
    }

    public static Map<String, Double> computeSubjectAverages(List<Pupil> group) {
        if (group == null || group.isEmpty()) {
            return Collections.emptyMap();
        }

        return group.stream()
                .flatMap(p -> p.getSubjects().stream()
                        .map(sub -> new SimpleEntry<>(sub, p.fetchGrade(sub))))
                .collect(Collectors.groupingBy(
                        Map.Entry::getKey,
                        Collectors.averagingInt(Map.Entry::getValue)
                ));
    }

    public static Set<String> listDistinctSubjects(List<Pupil> group) {
        if (group == null || group.isEmpty()) {
            return Collections.emptySet();
        }

        return group.stream()
                .flatMap(p -> p.getSubjects().stream())
                .collect(Collectors.toUnmodifiableSet());
    }

    public static void main(String[] args) {
        Pupil p1 = new Pupil(1, "Alice", List.of("Math", "Physics", "CS"), Map.of("Math", 90, "Physics", 85, "CS", 92));
        Pupil p2 = new Pupil(2, "Bob", List.of("Math", "CS"), Map.of("Math", 70));
        Pupil p3 = new Pupil(3, "Charlie", List.of("Physics", "Literature"), Map.of("Physics", 78, "Literature", 88));
        Pupil p4 = new Pupil(4, "Diana", List.of("Math", "Biology"), Map.of("Math", 95, "Biology", 90));
        Pupil p5 = new Pupil(5, "Eve", List.of("CS", "Literature"), Map.of("CS", 85, "Literature", 91));
        Pupil p6 = new Pupil(6, "Frank", List.of("Math", "Physics", "Biology"), Map.of("Math", 60, "Physics", 65, "Biology", 70));
        Pupil p7 = new Pupil(7, "Grace", List.of("Literature", "History"), Map.of("Literature", 99, "History", 95));
        Pupil p8 = new Pupil(8, "Hank", List.of("CS", "History"), Map.of("History", 80));
        Pupil p9 = new Pupil(9, "Ivy", List.of("Math", "Physics", "CS", "Biology"), Map.of("Math", 88, "Physics", 92, "CS", 95, "Biology", 89));
        Pupil p10 = new Pupil(10, "Jack", List.of("History", "Literature"), Map.of("History", 75, "Literature", 72));

        List<Pupil> students = List.of(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10);

        System.out.println("Top 3 Students:");
        findLeadingPerformers(students, 3).forEach(p -> 
            System.out.println(p.getFullName() + " (" + p.calculateMean() + ")"));
        
        System.out.println("\nAverage per course:");
        computeSubjectAverages(students).forEach((sub, avg) -> 
            System.out.println(sub + ": " + avg));
        
        System.out.println("\nUnique courses: " + listDistinctSubjects(students));
    }
}
